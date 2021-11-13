# -*- coding: utf-8 -*-

__all__ = (
    "OptionsDescription",
    "Placeholders",
    "EventsResponse",
    "CommandsDescription",
    "CommandsResponse",
    "Languages",
    "Regions",
    "Genres",
)


class Response(object):
    title: str
    description: str

    def __init__(self, title: str = None, description: str = None):
        self.title = title
        self.description = description


class OptionsDescription:
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


class Placeholders:
    menu = "Selecione uma das opções..."


class EventsResponse:
    cooldown = Response(
        title="Aguarde para usar o comando `{command_name}`",
        description="Por favor, aguarde {time:.2f} segundos para usar o comando",
    )
    not_found = Response(
        title="Nenhum resultado encontrado",
        description="Não foi possível encontrar nenhuma correspondência para essas especificações",
    )
    exception = Response(
        title="Ocorreu um erro inesperado com o comando `{command_name}`",
        description="Erro: {error}",
    )


class CommandsDescription:
    ping = "Obtenha a latência da PyPoca"
    help = "Veja o menu de ajuda da PyPoca"
    movie = "Tudo sobre filmes: encontre, descubra e obtenha informações"
    person = "Tudo sobre artistas: encontre, descubra e obtenha informações"
    tv = "Tudo sobre séries: encontre, descubra e obtenha informações"


class CommandsResponse:
    ping = Response(title="Pong!", description="Latência: {latency}ms")
    help = Response(
        title="Comandos disponíveis",
        description="Milhões de filmes, séries e artistas para descobrir. Explore agora!",
    )


class Languages:
    en_US = "Inglês"
    pt_BR = "Português"


class Regions:
    BR = "Brasil"
    US = "Estados Unidos"


class Genres:
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
