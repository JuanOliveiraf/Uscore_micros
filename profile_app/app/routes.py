from fastapi import APIRouter, HTTPException, Query, status
from typing import Optional
from app.models import Profile
from app.repository import ProfileRepository

router = APIRouter()
repo = ProfileRepository()

# Lista temporária de times de universidade (LEUP)
VALID_TEAMS = [
    "direito_fmu",
    "arquitetura_sao_judas",
    "caap_ufabc",
    "axis_ufabc",
    "fmu",
    "medicina_paulista",
    "direito_puc",
    "direito_sao_judas",
    "fea_puc",
    "faculdades_belas_artes",
    "medicina_maua",
    "faap",
    "nutricao_unicid",
    "engenharia_mackenzie",
    "engenharia_maua",
    "medicina_santa_casa",
    "uscs_imes",
    "saude_sao_judas",
    "faculdade_eniac",
    "faculdade_sao_camilo",
    "medicina_braganca",
    "unifsp",
    "medicina_sao_caetano",
    "lep_mackenzie",
    "ciencias_sociais_sao_judas",
    "negocios_anhembi_morumbi",
    "direito_mackenzie",
    "senac",
    "uni_italo",
    "psicologia_puc",
    "comunicacao_sao_judas",
    "espm",
    "medicina_guarulhos",
    "usp",
    "medicina_einstein",
    "tecnologia_sao_judas",
    "medicina_santo_amaro",
    "medicina_osasco",
    "insper",
    "liga_star",
    "eefe_usp",
    "pedagogia_usp",
    "medicina_abc",
    "economia_mackenzie"
]

# Lista temporária de competições
VALID_COMPETITIONS = [
    "leup",  # Liga Esportiva Universitária Paulista
    "brasileiro_universitario",
    "jogos_universitarios",
    "copa_universitaria"
]

@router.get("/")
def root():
    return {"service": "profileService", "status": "ok"}

@router.post("/api/profiles/", status_code=status.HTTP_201_CREATED)
def create_profile(profile: Profile):
    try:
        # Validação dos times favoritos
        for team in profile.favorite_teams:
            if team not in VALID_TEAMS:
                raise HTTPException(
                    status_code=400,
                    detail=f"Time inválido: '{team}'. Use GET /api/teams/ para ver times disponíveis."
                )
        
        # Validação das competições favoritas
        for comp in profile.favorite_competitions:
            if comp not in VALID_COMPETITIONS:
                raise HTTPException(
                    status_code=400,
                    detail=f"Competição inválida: '{comp}'. Use GET /api/competitions/ para ver competições disponíveis."
                )
        
        return repo.create(profile)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.get("/api/profiles/{user_id}")
def get_profile(user_id: str):
    doc = repo.get_by_user_id(user_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Profile not found")
    return doc

@router.put("/api/profiles/{user_id}")
def update_profile(user_id: str, profile: Profile):
    if user_id != profile.user_id:
        raise HTTPException(status_code=400, detail="user_id mismatch")
    
    # Validação dos times favoritos
    for team in profile.favorite_teams:
        if team not in VALID_TEAMS:
            raise HTTPException(
                status_code=400,
                detail=f"Time inválido: '{team}'. Use GET /api/teams/ para ver times disponíveis."
            )
    
    # Validação das competições favoritas
    for comp in profile.favorite_competitions:
        if comp not in VALID_COMPETITIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Competição inválida: '{comp}'. Use GET /api/competitions/ para ver competições disponíveis."
            )
    
    updated = repo.update(user_id, profile.model_dump(mode='json'))
    if not updated:
        raise HTTPException(status_code=404, detail="Profile not found")
    return updated

@router.delete("/api/profiles/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_profile(user_id: str):
    ok = repo.delete(user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Profile not found")

@router.get("/api/profiles/")
def list_profiles(q: Optional[str] = None, limit: int = 20, offset: int = 0):
    return repo.list_all(q, limit, offset)

# Endpoints para listar times e competições disponíveis
@router.get("/api/teams/")
def list_available_teams():
    """Lista todos os times de universidade disponíveis"""
    return {
        "teams": VALID_TEAMS,
        "total": len(VALID_TEAMS)
    }

@router.get("/api/competitions/")
def list_available_competitions():
    """Lista todas as competições disponíveis"""
    return {
        "competitions": VALID_COMPETITIONS,
        "total": len(VALID_COMPETITIONS)
    }

# Favoritos
@router.get("/api/profiles/{user_id}/favorites")
def list_favorites(user_id: str):
    doc = repo.get_by_user_id(user_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {
        "favorite_teams": doc.get("favorite_teams", []),
        "favorite_competitions": doc.get("favorite_competitions", [])
    }

@router.post("/api/profiles/{user_id}/favorites/teams/{team_id}")
def add_fav_team(user_id: str, team_id: str):
    # Validação: verifica se o time existe na lista
    if team_id not in VALID_TEAMS:
        raise HTTPException(
            status_code=400,
            detail=f"Time inválido. Escolha um time válido da LEUP."
        )
    
    doc = repo.add_favorite(user_id, "favorite_teams", team_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Profile not found")
    return doc

@router.delete("/api/profiles/{user_id}/favorites/teams/{team_id}")
def remove_fav_team(user_id: str, team_id: str):
    doc = repo.remove_favorite(user_id, "favorite_teams", team_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Profile not found")
    return doc

@router.post("/api/profiles/{user_id}/favorites/competitions/{competition_id}")
def add_fav_comp(user_id: str, competition_id: str):
    # Validação: verifica se a competição existe na lista
    if competition_id not in VALID_COMPETITIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Competição inválida. Escolha uma competição válida."
        )
    
    doc = repo.add_favorite(user_id, "favorite_competitions", competition_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Profile not found")
    return doc

@router.delete("/api/profiles/{user_id}/favorites/competitions/{competition_id}")
def remove_fav_comp(user_id: str, competition_id: str):
    doc = repo.remove_favorite(user_id, "favorite_competitions", competition_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Profile not found")
    return doc
