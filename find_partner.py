import random
from create_bot import USERS, queue
from aiogram import types, Dispatcher
from database import get_user, get_all_users, create_meeting


async def get_users_priorities(user_id, iterable):
    user = USERS[user_id] ### in future change to db
    priorities = {}
    for i in iterable:
        another_user = USERS[i]
        if user['grade'] == another_user['grade'] and user['speciality'] == another_user['speciality'] and user['user_group'] != another_user['user_group']:
            priorities[i] = 1
        elif user['grade'] == another_user['grade'] and user['speciality'] != another_user['speciality']:
            priorities[i] = 2
        elif user['grade'] == another_user['grade'] and user['speciality'] == another_user['speciality'] and user['user_group'] == another_user['user_group']:
            priorities[i] = 3
        elif user['grade'] != another_user['grade'] and user['speciality'] == another_user['speciality']:
            priorities[i] = 4
        elif user['grade'] != another_user['grade'] and user['speciality'] != another_user['speciality']:
            priorities[i] = 5
        else:
            priorities[i] = 6

    if priorities is None:
        return None

    return priorities


async def candidates(message: types.Message):
    user_id = str(message.from_user.id)
    priorities = await get_users_priorities(user_id, queue)  ### get candidates from queue

    user_from_queue = True

    if not priorities:  ### if not candidates in queue
        print('Not candidates in queue, check in not-queue users.')
        items = list(USERS.items())
        random.shuffle(items)
        users_shuffled = dict(items)

        priorities = await get_users_priorities(user_id, users_shuffled)
        user_from_queue = False

        if priorities is None:  ### if not candidates in not-in-queue users
            queue.add(user_id)
            print('Not any candidates for you, now you in queue.')
            return

    sorted_tuples = sorted(priorities.items(), key=lambda item: item[1])
    sorted_dict = {k: v for k, v in sorted_tuples}

    the_biggest_priority = sorted_dict[list(sorted_dict.keys())[0]]  ### 0 key value of sorted dict of candidates(the biggest priority)

    candidates_list = []

    for j in sorted_dict:
        if sorted_dict[j] != the_biggest_priority:
            break
        candidates_list.append(j)

    candidate_id = random.choice(candidates_list)
    if user_from_queue:
        queue.remove(candidate_id)
    print(f'candidate_id: {candidate_id}, queue: {queue}')
    await create_meeting(user_id, candidate_id, 'bla')


def register_meet_handlers(dp: Dispatcher):
    dp.register_message_handler(candidates, commands=['candidates'])




