from typing import List, Tuple

RGB8: int = 8
RGB16: int = 16

class CCFGenerator:
    def __init__(self, color_data: List[Tuple[Tuple[int, int, int], str]]):
        """
        ColorChartFile クラスを初期化します。

        :param color_data: RGBタプル (int, int, int) とラベル (str) を含むタプルのリスト
        """
        self.color_data: List[Tuple[Tuple[int, int, int], str]] = color_data

    def dec_to_hex_byte(self, value: int) -> bytes:
        """
        10進数の値を1バイトの16進数に変換します。

        :param value: 整数値 (0-255)
        :return: 値の16進数バイト表現
        """
        return value.to_bytes(1, 'big')

    def encode_label(self, label: str) -> bytes:
        """
        ラベルをエンコードします。英数字と記号はASCII、中国語、日本語の文字はGB18030でエンコードします。

        :param label: ラベル文字列
        :return: エンコードされたバイト列
        """
        encoded_bytes = bytearray()

        for char in label:
            # 英数字と記号はASCIIでエンコード
            if char.isascii():
                encoded_bytes.extend(char.encode('ascii'))
            else:
                encoded_bytes.extend(char.encode('gb18030')) # GB18030は、EUC-CNやEUC-JPに含まれない文字もサポート

        return bytes(encoded_bytes)

    def add_color_block(self, content: bytearray, rgb: Tuple[int, int, int], label: str) -> None:
        """
        色のブロックをバイト配列に追加します。

        :param content: バイト配列
        :param rgb: 8bit RGBタプル
        :param label: ラベル
        """
        r, g, b = rgb
        if r > 255 or g > 255 or b > 255:
            raise ValueError("RGB values must be in the range 0-255.")
        # 8bit RGB値を 16bit に変換し、それぞれの文字を2回繰り返す
        content.extend(self.dec_to_hex_byte(r) * 2)
        content.extend(self.dec_to_hex_byte(g) * 2)
        content.extend(self.dec_to_hex_byte(b) * 2)

        # ラベルをエンコード
        label_bytes = self.encode_label(label)
        label_bytes_length: int = len(label_bytes)  # エンコード後のバイト数
        if label_bytes_length > 15:
            label_bytes = label_bytes[:15]  # 15バイト以上の場合は切り捨て

        content.append(label_bytes_length)  # ラベルの長さ (ASCII形式) を追加

        # エンコードされたラベルを追加
        content.extend(label_bytes)

        # 文字ブロック長を16バイトにするためにゼロでパディング
        padding_length: int = 15 - label_bytes_length
        if padding_length > 0 and label_bytes_length < 15:
            content.extend([0] * padding_length)

    def fill_to_target_length(self, content: bytearray, target_length: int) -> None:
        """
        指定された長さまでバイト配列を埋めます。

        :param content: バイト配列
        :param target_length: 目標の長さ
        """
        content.extend([0xFF] * 6)
        fill_pattern: List[int] = [0] * 16 + [0xFF] * 6
        fill_length = target_length - len(content) - 16  # 最後の16個のゼロを除外

        if fill_length > 0:
            full_patterns, extra_bytes = divmod(fill_length, len(fill_pattern))
            content.extend(fill_pattern * full_patterns)
            content.extend(fill_pattern[:extra_bytes])

        # 最後の16個のゼロを追加
        content.extend([0] * 16)

    def create_ccf_file(self, output_file_path: str) -> None:
        """
        カラーチャートファイル (CCF) を作成し、指定されたファイルパスに保存します。

        :param output_file_path: CCFファイルを保存するファイルパス
        """
        content: bytearray = bytearray()
        # ファイルヘッダーを追加
        content.append(0)  # SOH
        content.extend(self.dec_to_hex_byte(100))  # d

        # 各色とラベルをバイト配列に追加
        for rgb, label in self.color_data:
            self.add_color_block(content, rgb, label)

        # バイト配列を0x6E01まで埋める
        target_length: int = 0x6E01
        self.fill_to_target_length(content, target_length)

        content.append(0)  # 終端のバイトを追加

        # ファイルに書き込む
        with open(output_file_path, 'wb') as file:
            file.write(content)

class CCFReader:
    def __init__(self, file_path: str):
        """
        CCFFileReader クラスを初期化します。

        :param file_path: 読み込む CCF ファイルのパス
        """
        self.file_path: str = file_path

    def hex_byte_to_dec(self, byte_data: bytes) -> int:
        """
        16進数バイトを10進数に変換します。

        :param byte_data: 1バイトのデータ
        :return: 10進数の整数値
        """
        return int.from_bytes(byte_data, 'big')

    def decode_label(self, label_bytes: bytes) -> str:
        """
        ラベルをデコードします。英数字と記号はASCII、中国語、日本語の文字はGB18030でデコードします。

        :param label_bytes: エンコードされたラベルのバイト列
        :return: デコードされたラベル文字列
        """
        decoded_label = ""
        i = 0
        while i < len(label_bytes):
            if label_bytes[i] <= 127:  # ASCII範囲内の場合
                decoded_label += label_bytes[i:i + 1].decode('ascii')
                i += 1
            else:
                try:
                    # GB18030でデコード
                    decoded_label += label_bytes[i:i + 2].decode('gb18030') # GB18030は、EUC-CNやEUC-JPに含まれない文字をサポート
                    i += 2
                except UnicodeDecodeError as e:
                    print(f"UnicodeDecodeError: {e}")
                    break

        return decoded_label

    def read_ccf_file(self,
                      color_depth: int = RGB8,
                      ) -> List[Tuple[str, Tuple[int, int, int]]]:
        """
        CCFファイルを読み込み、色名とRGB値のリストを返します。

        :param color_depth: 色の深さ (8bit または 16bit)。デフォルトは 8bit

        :return: (色名, RGB値) のタプルのリスト
        """
        color_data: List[Tuple[str, Tuple[int, int, int]]] = []

        with open(self.file_path, 'rb') as file:
            # 読み込み開始（最初の2バイトはヘッダーなのでスキップ）
            file.read(2)

            while True:
                # RGB値を読み取る（16bit RGB）
                r_bytes = file.read(2)
                g_bytes = file.read(2)
                b_bytes = file.read(2)

                # 終端に達した場合、ループを終了
                if not r_bytes or not g_bytes or not b_bytes:
                    break

                # RGB値を10進数に変換
                r = self.hex_byte_to_dec(r_bytes)
                g = self.hex_byte_to_dec(g_bytes)
                b = self.hex_byte_to_dec(b_bytes)

                # ラベル長を読み取り
                label_length = self.hex_byte_to_dec(file.read(1))

                # ラベルを読み取り、デコード
                label_bytes = file.read(label_length)
                label = self.decode_label(label_bytes)

                # 8bit RGBの場合
                if color_depth == 8:
                    # 16-bit RGBを8-bitに変換
                    r = r >> 8
                    g = g >> 8
                    b = b >> 8

                # 色データをリストに追加
                color_data.append((label, (r, g, b)))

                # パディングをスキップして次の色ブロックへ（15バイトに合わせるための0パディング）
                padding_length = 15 - label_length
                file.read(padding_length)

        if color_depth == 16:
            # 16-bit RGBの場合、純白は (65535, 65535, 65535)
            filtered_data = [
                (label, rgb) for label, rgb in color_data
                if not (label == "" and rgb == (65535, 65535, 65535))
            ]
        elif color_depth == 8:
            # 8-bit RGBの場合、純白は (255, 255, 255)
            filtered_data = [
                (label, rgb) for label, rgb in color_data
                if not (label == "" and rgb == (255, 255, 255))
            ]
        else:
            filtered_data = color_data

        return filtered_data
