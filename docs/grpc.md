# gRPC API (Database Service)

## Proto
database/proto/database.proto

Service methods:
- ChangeAccess(telegram_id, group_id) -> { ok }
- IsOwner(telegram_id) -> { ok }
- IsAdmin(telegram_id) -> { ok }
- DeleteItem(telegram_id, hash_name) -> { ok }
- UserItems(telegram_id) -> { items: map<string, int32> }
- AddLog(telegram_id, username, function_name) -> { ok }

## Messages
- ChangeAccessRequest { int64 telegram_id; int32 group_id; }
- IsAccessRequest { int64 telegram_id; }
- DeleteItemRequest { int64 telegram_id; string hash_name; }
- UserItemsRequest { int64 telegram_id; }
- AddLogRequest { int64 telegram_id; string username; string function_name; }

## Client usage (bot)
- Address: DATABASE_GRPC_ADDR (e.g., database:50051)
- Client: bot/src/services/database_client.py
- Methods: change_access, is_owner, is_admin, delete_item, user_items, add_log

## Running server
- Compose: docker-compose.yaml has database service; set DATABASE_DSN
- Server entrypoint: database/src/server.py

## Notes
- Bot actions call gRPC conditionally (only if DATABASE_GRPC_ADDR is set)
- Database session is created via a generator with context manager
