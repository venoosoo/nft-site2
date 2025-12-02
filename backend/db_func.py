import aiosqlite

DB_PATH = "gifts.db"

#=============================GIFTS==================================#
async def get_random_row():
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        cur = await conn.cursor()
        await cur.execute("SELECT collection, gift_id, price FROM gifts ORDER BY RANDOM() LIMIT 1;")
        row = await cur.fetchone()
        return dict(row) if row else None

#=============================USERS==================================#


async def new_user(user_id: int) -> bool:
    try:
        async with aiosqlite.connect(DB_PATH) as conn:
            cur = await conn.cursor()

            await cur.execute("SELECT 1 FROM Users WHERE user_id = ? LIMIT 1", (user_id,))
            exists = await cur.fetchone()
            if exists:
                return False  

            await cur.execute(
                "INSERT INTO Users (user_id) VALUES (?)",
                (user_id,)
            )

            await conn.commit()
            return True

    except Exception as e:
        print("DB error:", e)
        return False





async def save_num_user(user_id: int, phone_number: str) -> bool:
    try:
        async with aiosqlite.connect(DB_PATH) as conn:
            cur = await conn.cursor()

            await cur.execute(
                "UPDATE Users SET phone_number = ? WHERE user_id = ?",
                (phone_number, user_id)
            )

            await conn.commit()
            return True

    except Exception as e:
        print("DB error:", e)
        return False



async def put_2fa_in_user(user_id, two_fa):
    try:
        async with aiosqlite.connect(DB_PATH) as conn:
            cur = await conn.cursor()

            await cur.execute(
                "UPDATE users SET two_fa = ? WHERE user_id = ?",
                (two_fa, user_id)
            )

            await conn.commit()
            return True

    except Exception as e:
        print("DB error:", e)
        return False


async def get_num_from_id(user_id):
    try:
        async with aiosqlite.connect(DB_PATH) as conn:
            cur = await conn.cursor()
            await cur.execute("SELECT phone_number FROM Users WHERE user_id = ?", (user_id,))
            row = await cur.fetchone()
            if row:
                return row[0]  # return the phone number as string
            return None
    except Exception as e:
        print("DB error:", e)
        return None