# -*- coding: utf-8 -*-

__all__ = (
    "DATETIME_STR",
    "OptionDescription",
    "Placeholder",
    "EventReply",
    "CommandDescription",
    "CommandReply",
    "Language",
    "Region",
    "Genre",
)

DATETIME_STR = "%d/%m/%Y"


class Reply:
    """Basic reply model."""

    title: str
    description: str

    def __init__(self, title: str = None, description: str = None):
        self.title = title
        self.description = description


class OptionDescription:
    """All available option descriptions with the respectives regionalized name."""

    query = "Uma consulta de texto para pesquisar"
    page = "Especifique qual página consultar"
    language = "Um valor ISO 639-1 para exibir os dados traduzidos"
    region = "Um código ISO 3166-1 para filtrar datas de lançamento"
    nsfw = "Escolha se deseja incluir conteúdo adulto (pornografia) nos resultados"
    sort_by = "Escolha uma das muitas opções de classificação disponíveis"
    year = "Incluir apenas resultados com uma data de lançamento igual ao valor especificado"
    min_year = "Incluir apenas resultados com uma data de lançamento maior ou igual ao valor especificado"
    max_year = "Incluir apenas resultados com uma data de lançamento menor ou igual ao valor especificado"
    min_votes = "Incluir apenas resultados com contagem de votos maior ou igual ao valor especificado"
    max_votes = "Incluir apenas resultados com contagem de votos menor ou igual ao valor especificado"
    min_rating = "Incluir apenas resultados com classificação maior ou igual ao valor especificado"
    max_rating = "Incluir apenas resultados com classificação menor ou igual ao valor especificado"
    min_runtime = "Incluir apenas resultados com uma duração maior ou igual a um valor"
    max_runtime = "Incluir apenas resultados com uma duração menor ou igual a um valor"
    interval = "Veja a lista de tendências do dia ou semana"
    hide = "A resposta do comando só será visível para você"
    service = "Filtrar os resultados por serviço de streaming ou canal específico"


class Placeholder:
    """All available placeholders with the respectives regionalized name."""

    menu = "Selecione uma das opções..."


class EventReply:
    """All available event replies with the respectives regionalized name."""

    cooldown = Reply(
        title="Aguarde para usar o comando `{command_name}`",
        description="Por favor, aguarde {time:.2f} segundos para usar o comando",
    )
    not_found = Reply(
        title="Nenhum resultado encontrado",
        description="Não foi possível encontrar nenhuma correspondência para essas especificações",
    )
    exception = Reply(
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
    popular_movie = "Veja os filmes mais populares"
    search_movie = "Pesquise por um filme"
    top_movie = "Veja os filmes com melhor nota de todos os tempos"
    trending_movie = "Veja os filmes da tendência"
    upcoming_movie = "Veja os próximos filmes nos cinemas"


class CommandReply:
    """All available command replies with the respectives regionalized name."""

    ping = Reply(title="Pong!", description="Latência: {latency}ms")
    help = Reply(
        title="Comandos disponíveis",
        description="Milhões de filmes, séries e artistas para descobrir. Explore agora!",
    )


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

    action = "Ação"
    action_and_adventure = "Ação & Aventura"
    adventure = "Aventura"
    animation = "Animação"
    comedy = "Comédia"
    crime = "Crime"
    documentary = "Documentário"
    drama = "Drama"
    family = "Família"
    fantasy = "Fantasia"
    history = "História"
    horror = "Terror"
    kids = "Infantil"
    music = "Musical"
    mystery = "Mistério"
    news = "Notícia"
    reality = "Reality Show"
    romance = "Romance"
    soap = "Soap"
    syfy = "Ficção científica"
    syfy_and_fantasy = "Ficção científica & Fantasia"
    talk = "Talk Show"
    tv = "Cinema TV"
    thriller = "Thriller"
    war = "Guerra"
    war_and_politics = "Guerra & Política"
    western = "Faroeste"
