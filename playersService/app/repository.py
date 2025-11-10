from typing import List, Optional
from datetime import datetime
from tinydb import Query
from app.database import get_database
from app.models import PlayerCreate, PlayerUpdate, PlayerInDB
import re


class PlayerRepository:
    def __init__(self):
        self.table_name = "players"

    def get_table(self):
        db = get_database()
        return db.table(self.table_name)

    async def create_player(self, player: PlayerCreate) -> PlayerInDB:
        table = self.get_table()
        now = datetime.utcnow().isoformat()
        
        player_dict = player.model_dump()
        player_dict["created_at"] = now
        player_dict["updated_at"] = now
        
        # TinyDB retorna o ID do documento inserido
        doc_id = table.insert(player_dict)
        
        # Buscar o documento recém-criado
        created_player = table.get(doc_id=doc_id)
        created_player["_id"] = str(doc_id)
        
        return PlayerInDB(**created_player)

    async def get_player(self, player_id: str) -> Optional[PlayerInDB]:
        table = self.get_table()
        
        try:
            # TinyDB usa inteiros como IDs
            player_id_int = int(player_id)
        except (ValueError, TypeError):
            return None
            
        player = table.get(doc_id=player_id_int)
        
        if player:
            player["_id"] = str(player_id_int)
            return PlayerInDB(**player)
        return None

    async def get_all_players(self, skip: int = 0, limit: int = 100) -> List[PlayerInDB]:
        table = self.get_table()
        # TinyDB retorna lista de documentos
        all_players = table.all()
        
        # Aplicar paginação manualmente
        paginated_players = all_players[skip:skip + limit]
        
        players = []
        for player in paginated_players:
            # TinyDB usa .doc_id para o ID do documento
            player["_id"] = str(player.doc_id)
            players.append(PlayerInDB(**player))
        
        return players

    async def update_player(self, player_id: str, player_update: PlayerUpdate) -> Optional[PlayerInDB]:
        table = self.get_table()
        
        try:
            player_id_int = int(player_id)
        except (ValueError, TypeError):
            return None
        
        update_data = player_update.model_dump(exclude_unset=True)
        
        if not update_data:
            return await self.get_player(player_id)
        
        update_data["updated_at"] = datetime.utcnow().isoformat()
        
        # TinyDB update
        result = table.update(update_data, doc_ids=[player_id_int])
        
        if not result:
            return None
            
        return await self.get_player(player_id)

    async def delete_player(self, player_id: str) -> bool:
        table = self.get_table()
        
        try:
            player_id_int = int(player_id)
        except (ValueError, TypeError):
            return False
            
        result = table.remove(doc_ids=[player_id_int])
        return len(result) > 0

    async def search_players(self, query: str) -> List[PlayerInDB]:
        table = self.get_table()
        
        # TinyDB - busca manual com regex
        all_players = table.all()
        pattern = re.compile(query, re.IGNORECASE)
        
        players = []
        for player in all_players:
            # Buscar em nome, email, team ou position
            if (pattern.search(player.get("name", "")) or
                pattern.search(player.get("email", "")) or
                pattern.search(player.get("team", "")) or
                pattern.search(player.get("position", ""))):
                player["_id"] = str(player.doc_id)
                players.append(PlayerInDB(**player))
        
        return players


player_repository = PlayerRepository()
