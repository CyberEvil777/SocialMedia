from fastapi import HTTPException


def get_404_exception(rowcount):
    """Функция выдает 404, если rowcount=0
    rowcount принимает заначение 0, если запрос в БД был не выполнен"""
    if not rowcount:
        raise HTTPException(status_code=404, detail="Объект не найден")