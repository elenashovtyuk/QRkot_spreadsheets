# чтобы SQLAlchemy узнала обо всех моделях до того, как
# начнут выстраиваться взаимосвязи между ними, нужно импортировать все модели в файл init
from .charity_projects import CharityProject # noqa
from .donation import Donation # noqa
from .user import User # noqa
