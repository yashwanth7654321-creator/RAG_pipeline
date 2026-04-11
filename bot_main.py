from source_code.database import create_db, create_table
from source_code.cache_DB import create_cache_DB
from source_code.bot import run_bot
from config import BOT_TOKEN


def main():
    conn, cursor = create_db()
    create_table(conn, cursor)
    client, collection = create_cache_DB()
    print("Bot is starting...")
    run_bot(BOT_TOKEN, conn, cursor, collection)


if __name__ == "__main__":
    main()