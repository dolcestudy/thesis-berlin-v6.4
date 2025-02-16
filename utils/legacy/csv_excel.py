import pandas as pd

# CSV.gz ファイルのパス
input_file = r"C:\berlin\output\micro080pct-sp45-pce0.5-DMC-2.5-MDR-0.24-iter0\output_links.csv.gz"

# 出力する Excel ファイルのパス
output_file = r"C:\berlin\output\micro080pct-sp45-pce0.5-DMC-2.5-MDR-0.24-iter0\output_links.xlsx"

# CSV.gz を読み込み
# `sep=';'` は区切り文字がセミコロンであることを指定
try:

    # データ型を明示的に指定
    dtype_spec = {
        13: 'str',  # 列13を文字列として読み込む
        17: 'str',  # 列17を文字列として読み込む
    }

    df = pd.read_csv(input_file, sep=';', compression='gzip', dtype=dtype_spec)

    # データフレームを Excel ファイルとして保存
    df.to_excel(output_file, index=False)
    print(f"Excel ファイルとしてエクスポートしました: {output_file}")

except Exception as e:
    print(f"エラーが発生しました: {e}")
