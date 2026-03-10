'''
python seed.py
'''

import os
from dotenv import load_dotenv

# .envファイルを最初に読み込むことが重要です
load_dotenv()

# 環境変数を読み込んだ後に、アプリケーションのモジュールをインポートします
from database import SessionLocal, engine
from models import Base, User, Category, Document
from auth import get_hashed_password

# --- ここに登録したい固定データを定義します ---

# ユーザーデータ (パスワードはすべて 'password' です)
USERS_DATA = [
    {"username": "user1", "password": get_hashed_password("password")},
    {"username": "user2", "password": get_hashed_password("password")},
    {"username": "user3", "password": get_hashed_password("password")},
    {"username": "user4", "password": get_hashed_password("password")},
]

# カテゴリデータ
CATEGORIES_DATA = [
    {"id": 1, "name": "出欠・連絡関連"},
    {"id": 2, "name": "研修プログラム・システム"},
    {"id": 3, "name": "その他・FAQ"},
]

# ドキュメントデータ (category_idでカテゴリと関連付け)
DOCUMENTS_DATA = [
    # --- カテゴリ1: 出欠・連絡関連 ---
    {
        "category_id": 1,
        "title": "研修を欠席する場合の連絡方法",
        "content": "研修を欠席する場合は、研修開始時刻までに担当者（training_admin@example.com）へメールで連絡してください。件名は「【欠席連絡】[氏名]」としてください。",
    },
    {
        "category_id": 1,
        "title": "研修に遅刻する場合の手順",
        "content": "公共交通機関の遅延など、やむを得ない事情で遅刻する場合は、判明した時点ですぐに担当者へ社内チャットツールで連絡してください。",
    },
    {
        "category_id": 1,
        "title": "研修中の早退・中抜けについて",
        "content": "体調不良等で早退または一時的に席を外す（中抜け）場合は、講師に口頭で伝えた上で、担当者にもチャットで一報ください。",
    },
    {
        "category_id": 1,
        "title": "緊急連絡先一覧",
        "content": "研修担当: 研修事務局 (内線: 1234), メール: training_admin@example.com. 緊急時は人事部 (内線: 5678) までご連絡ください。",
    },
    {
        "category_id": 1,
        "title": "連絡の基本ルール",
        "content": "連絡は原則として社内チャットツールを使用してください。ただし、正式な依頼や記録を残す必要がある場合はメールを使用します。",
    },
    {
        "category_id": 1,
        "title": "研修期間中の休暇取得について",
        "content": "研修期間中の休暇取得は原則として認められません。ただし、冠婚葬祭など特別な事情がある場合は、事前に上長および研修担当へ相談してください。",
    },
    {
        "category_id": 1,
        "title": "連絡がつかない場合の対応",
        "content": "無断での欠席・遅刻が続く場合、上長および人事部へ報告の上、状況確認を行います。",
    },
    # --- カテゴリ2: 研修プログラム・システム ---
    {
        "category_id": 2,
        "title": "2024年度 新入社員研修プログラム概要",
        "content": "本研修は3ヶ月間のプログラムです。最初の1ヶ月はビジネスマナーとIT基礎知識、後半2ヶ月は各部署に配属されてのOJT形式となります。",
    },
    {
        "category_id": 2,
        "title": "使用するオンライン研修システムについて",
        "content": "本研修では「KnowledgeHub」システムを使用します。ログインIDとパスワードは別途メールで通知します。URL: https://knowledge-hub.example.com",
    },
    {
        "category_id": 2,
        "title": "研修資料のダウンロード方法",
        "content": "研修資料はすべて「KnowledgeHub」システム上の「資料」セクションからダウンロード可能です。事前にダウンロードして研修に臨んでください。",
    },
    {
        "category_id": 2,
        "title": "課題の提出方法と期限",
        "content": "各単元の最後に出される課題は、指定された期限までにシステム経由で提出してください。期限を過ぎると提出できなくなりますのでご注意ください。",
    },
    {
        "category_id": 2,
        "title": "研修システムのトラブルシューティング",
        "content": "システムにログインできない、動画が再生されない等の問題が発生した場合は、まずキャッシュのクリアとブラウザの再起動を試してください。解決しない場合は、ITヘルプデスクへ連絡してください。",
    },
    {
        "category_id": 2,
        "title": "OJT期間の進め方",
        "content": "OJT期間中は、配属先のトレーナーの指示に従ってください。日報を毎日提出し、週に一度の1on1で進捗を確認します。",
    },
    {
        "category_id": 2,
        "title": "最終発表会について",
        "content": "研修の最後には、研修の成果を発表する最終発表会が開催されます。詳細は研修の最終月にアナウンスされます。",
    },
    # --- カテゴリ3: その他・FAQ ---
    {
        "category_id": 3,
        "title": "研修期間中の服装について",
        "content": "研修期間中の服装はビジネスカジュアルを基本とします。ただし、社外の方と接する機会がある場合はスーツを着用してください。",
    },
    {
        "category_id": 3,
        "title": "昼食について",
        "content": "昼食は各自でご用意ください。研修会場近くの社員食堂も利用可能です。研修会場内での食事も可能ですが、匂いの強いものはご遠慮ください。",
    },
    {
        "category_id": 3,
        "title": "貸与PCの取り扱いについて",
        "content": "研修用のPCは会社からの貸与品です。業務外での使用や、許可されていないソフトウェアのインストールは禁止です。紛失・破損した場合は速やかに報告してください。",
    },
    {
        "category_id": 3,
        "title": "研修中の質問方法",
        "content": "研修内容に関する質問は、各講義のQ&A時間または研修システムのフォーラムをご利用ください。事務的な質問は研修担当者へお願いします。",
    },
    {
        "category_id": 3,
        "title": "交通費の精算について",
        "content": "研修会場までの交通費は、経費精算システムを利用して月末にまとめて申請してください。申請にはICカードの利用履歴が必要です。",
    },
    {
        "category_id": 3,
        "title": "研修評価について",
        "content": "研修の評価は、課題提出、理解度テスト、最終発表、研修態度などを総合的に判断します。評価結果は配属後の育成計画に活用されます。",
    },
]


def seed_data():
    """データベースに初期データを投入する関数"""
    print("データベースに初期データを投入します...")
    db = SessionLocal()
    try:
        # 既存データがある場合は投入しないように簡単なチェック
        if db.query(User).count() == 0:
            print("  - ユーザーデータを追加します...")
            for data in USERS_DATA:
                db.add(User(**data))
            db.commit()

        if db.query(Category).count() == 0:
            print("  - カテゴリデータを追加します...")
            for data in CATEGORIES_DATA:
                db.add(Category(**data))
            db.commit()

        if db.query(Document).count() == 0:
            print("  - ドキュメントデータを追加します...")
            for data in DOCUMENTS_DATA:
                db.add(Document(**data))
            db.commit()

        print("データの投入が完了しました。")

    except Exception as e:
        print(f"エラーが発生しました: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    # スクリプトとして直接実行された場合にのみ実行
    print("テーブル定義を確認・作成します...")
    # データベースとテーブルがなければ作成
    Base.metadata.create_all(bind=engine)
    
    # データ投入関数を呼び出し
    seed_data()
