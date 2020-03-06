run jupyterlab server for debug

```bash
PYTHONPATH=$PYTHONPATH:`pwd` pipenv run jupyter lab --log-level=DEBUG --notebook-dir=notebooks
```

# カードデータベースのメンテナンス

## データベースマイグレーション

### 初期設定

まずはコマンドを実行して雛形を作る。
```bash
pipenv run alembic init migrate
```

次に、`alembic.ini`を編集する。こうなっているところを
```alembic.ini
sqlalchemy.url = driver://user:pass@localhost/dbname
```

こうする。
```alembic.ini
sqlalchemy.url = sqlite:///crawling.sqlite3
```

さらに、`migrate/env.py`を編集する。こうなっているところを
```migrate/env.py
target_metadata = None
```

こうする。
```migrate/env.py
from pyugo_db.models import Base
target_metadata = Base.metadata
```
### リビジョンの追加

```bash
PYTHONPATH=$PYTHONPATH:`pwd` pipenv run alembic --config alembic.ini revision --autogenerate
```

### 最新版のリビジョンを適用
```bash
PYTHONPATH=$PYTHONPATH:`pwd` pipenv run alembic --config alembic.ini upgrade head
```
