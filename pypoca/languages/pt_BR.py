# -*- coding: utf-8 -*-

__all__ = (
    "DATETIME_FORMAT",
    "FALSE",
    "PLACEHOLDER",
    "TRUE",
    "Button",
    "CommandDescription",
    "CommandReply",
    "EventReply",
    "Field",
    "Genre",
    "Interval",
    "Language",
    "Option",
    "Region",
    "Sort",
)

DATETIME_FORMAT = "%d/%m/%Y"
PLACEHOLDER = "Selecione uma das opções..."
TRUE = "sim"
FALSE = "não"


class Object:
    """Basic object title-description model."""

    title: str
    description: str

    def __init__(self, title: str = None, description: str = None):
        self.title = title
        self.description = description


class Option:
    """All available option descriptions with the respectives regionalized name."""

    query = Object(
        title="nome",
        description="Uma consulta de texto para pesquisar",
    )
    page = Object(
        title="página",
        description="Especifique qual página consultar",
    )
    language = Object(
        title="idioma",
        description="Um valor ISO 639-1 para exibir os dados traduzidos",
    )
    region = Object(
        title="região",
        description="Um código ISO 3166-1 para filtrar datas de lançamento",
    )
    nsfw = Object(
        title="adulto",
        description="Escolha se deseja incluir conteúdo adulto (pornografia) nos resultados",
    )
    sort_by = Object(
        title="ordem",
        description="Escolha uma das muitas opções de classificação disponíveis",
    )
    year = Object(
        title="ano",
        description="Incluir apenas resultados com uma data de lançamento igual ao valor especificado",
    )
    min_year = Object(
        title="ano-mínimo",
        description="Incluir apenas resultados com uma data de lançamento maior ou igual ao valor especificado",
    )
    max_year = Object(
        title="ano-máximo",
        description="Incluir apenas resultados com uma data de lançamento menor ou igual ao valor especificado",
    )
    min_votes = Object(
        title="votos-mínimos",
        description="Incluir apenas resultados com contagem de votos maior ou igual ao valor especificado",
    )
    max_votes = Object(
        title="votos-máximos",
        description="Incluir apenas resultados com contagem de votos menor ou igual ao valor especificado",
    )
    min_rating = Object(
        title="nota-mínima",
        description="Incluir apenas resultados com classificação maior ou igual ao valor especificado",
    )
    max_rating = Object(
        title="nota-máxima",
        description="Incluir apenas resultados com classificação menor ou igual ao valor especificado",
    )
    min_runtime = Object(
        title="duração-mínima",
        description="Incluir apenas resultados com uma duração maior ou igual a um valor",
    )
    max_runtime = Object(
        title="duração-máxima",
        description="Incluir apenas resultados com uma duração menor ou igual a um valor",
    )
    interval = Object(
        title="intervalo",
        description="Escolha entre as tendências do dia ou semana",
    )
    hide = Object(
        title="esconder",
        description="A resposta do comando será visível apenas para você",
    )
    service = Object(
        title="serviço",
        description="Filtrar os resultados por serviço de streaming ou canal específico",
    )
    genre = Object(
        title="gênero",
        description="Filtrar os resultados por um gênero específico",
    )


class EventReply:
    """All available event replies with the respectives regionalized name."""

    cooldown = Object(
        title="Aguarde para usar o comando `{command_name}`",
        description="Por favor, aguarde {time:.2f} segundos para usar o comando",
    )
    not_found = Object(
        title="Nenhum resultado encontrado",
        description="Não foi possível encontrar nenhuma correspondência para essas especificações",
    )
    exception = Object(
        title="Ocorreu um erro inesperado com o comando `{command_name}`",
        description="Erro: {error}",
    )


class CommandDescription:
    """All available command descriptions with the respectives regionalized name."""

    ping = "Obtenha a latência da PyPoca"
    help = "Veja o menu de ajuda da PyPoca"
    movie = "Tudo sobre filmes: encontre, descubra e obtenha informações"
    person = "Tudo sobre artistas: encontre, descubra e obtenha informações"
    tv = "Tudo sobre séries: encontre, descubra e obtenha informações"
    discover_movie = "Descubra filmes por diferentes tipos de filtros"
    discover_tv = "Descubra séries por diferentes tipos de filtros"
    popular_movie = "Veja os filmes mais populares"
    popular_person = "Veja os artistas mais populares"
    popular_tv = "Veja os séries mais populares"
    search_movie = "Pesquise por um filme"
    search_person = "Pesquise por um artista"
    search_tv = "Pesquise por um seriado"
    top_movie = "Veja os filmes com melhor nota"
    top_tv = "Veja os séries com melhor nota"
    trending_movie = "Veja os filmes da tendência"
    trending_person = "Veja os artistas da tendência"
    trending_tv = "Veja os séries da tendência"
    upcoming_movie = "Veja os próximos filmes nos cinemas"
    upcoming_tv = "Veja os próximos seriado a serem lançados"


class CommandReply:
    """All available command replies with the respectives regionalized name."""

    ping = Object(title="Pong!", description="Latência: {latency}ms")
    help = Object(
        title="Comandos disponíveis",
        description="Milhões de filmes, séries e artistas para descobrir. Explore agora!",
    )
    movie = Object(title="Filmes encontrados")
    tv = Object(title="Séries encontrados")
    person = Object(title="Artistas encontrados")


class Language:
    """All available languages with the respectives regionalized name."""

    en_US = "Inglês"
    pt_BR = "Português"


class Region:
    """All available regions with the respectives regionalized name."""

    BR = "Brasil"
    US = "Estados Unidos"


class Genre:
    """All available genres with the respectives regionalized name."""

    action = "ação"
    action_and_adventure = "ação & aventura"
    adventure = "aventura"
    animation = "animação"
    comedy = "comédia"
    crime = "crime"
    documentary = "documentário"
    drama = "drama"
    family = "família"
    fantasy = "fantasia"
    history = "história"
    horror = "terror"
    kids = "infantil"
    music = "musical"
    mystery = "mistério"
    news = "notícia"
    reality = "reality show"
    romance = "romance"
    soap = "soap"
    syfy = "ficção científica"
    syfy_and_fantasy = "ficção científica & fantasia"
    talk = "talk show"
    tv = "TV"
    thriller = "thriller"
    war = "guerra"
    war_and_politics = "guerra & política"
    western = "faroeste"


class Sort:
    """All available orderings with the respectives regionalized name."""

    popularity = "popularidade"
    year = "lançamento"
    rating = "nota"
    title = "alfabética"
    votes = "votos"


class Interval:
    """All available intervals with the respectives regionalized name."""

    day = "dia"
    week = "semana"


class Button:
    """All available buttons with the respectives regionalized name."""

    invite = "Adicionar"
    vote = "Votar"
    server = "Servidor"
    github = "Github"


class Field:
    """All available fields with the respectives regionalized name."""

    acting = "Atuações"
    birthday = "Aniversário"
    born = "Naturalidade"
    cast = "Elenco"
    crew = "Equipe"
    deathday = "Falecimento"
    episodes = "Episódios"
    genre = "Gêneros"
    know_for = "Trabalhou em"
    jobs = "Trabalhos"
    network = "Rede"
    premiered = "Estreia"
    rating = "Nota"
    released = "Lançamento"
    runtime = "Duração"
    seasons = "Temporadas"
    similar = "Similares"
    studios = "Estúdios"
    trailer = "Trailer"
    watch = "Assista em"
