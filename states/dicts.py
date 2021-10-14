from .states import *

CATEGORIES = {
    "🍍 Еда":
    {
        "id" : 1000,
    },

    "🏃‍ Тренировки":
    {
        "id" : 2000,
    },
    "🎳 Другое":
    {
        "id": 3000,
    }

}


states_switch = {
    0:
    {
        "state": States.name,
        "name": "name",
    },
    1:
    {
        "state": States.surname,
        "name": "surname",
    },
    2:
    {
        "state": States.date,
        "name": "date",
    },
    3:
    {
        "state": States.gender,
        "name": "gender",
    },
}

request_status_switch = {
    0: "Status: In process",
    1: "Status: Accepted",
    -1: "Status: Declined",

}
