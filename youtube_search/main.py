import json
import os
from datetime import datetime

from googleapiclient.discovery import build

SEARCH_RESULTS_FILE = "search_results.json"
YT_API_KEY = os.getenv('YT_API_KEY')
RESULTS_COUNT = 10
OPTIONS = {
    'n': 'ввести новый запрос',
    'w': 'сохранить результаты в файл JSON и ввести новый запрос',
    'wq': 'сохранить результаты в файл JSON и выйти',
    'q': 'выйти'
}


def get_youtube_service() -> build:
    """Создает и возвращает объект YouTube API service, используя ключ API из переменной окружения."""
    youtube = build('youtube', 'v3', developerKey=YT_API_KEY)
    return youtube


def get_search_results(query: str) -> list[dict]:
    """Выполняет поиск видео в YouTube по заданному запросу и возвращает список видео."""

    youtube = get_youtube_service()
    search_response = youtube.search().list(
        q=query,
        type='video',
        part='id,snippet',
        maxResults=RESULTS_COUNT
    ).execute()

    videos = []
    for search_result in search_response.get('items', []):
        video_id = search_result['id']['videoId']
        video_info = youtube.videos().list(
            id=video_id,
            part='snippet,statistics'
        ).execute()

        video = {
            'video_id': video_id,
            'title': video_info['items'][0]['snippet']['title'],
            'channel_title': video_info['items'][0]['snippet']['channelTitle'],
            'view_count': int(video_info['items'][0]['statistics']['viewCount']),
            'like_count': int(video_info['items'][0]['statistics']['likeCount'])
        }
        videos.append(video)

    return videos


def format_video_info(video_info: dict) -> dict:
    """Форматирует информацию о видео для вывода в консоль и возвращает словарь со всей информацией о видео."""

    formatted_video_info = {
        'title': f"{video_info['title'][:35]}..." if len(video_info['title']) > 35 else video_info['title'],
        'view_count': video_info['view_count'],
        'like_count': video_info['like_count'],
        'ratio': f"{round(video_info['ratio'] * 100, 1)} %",
        'url': f"<https://www.youtube.com/watch?v={video_info['video_id']}>"
    }
    return formatted_video_info


def print_table_header() -> None:
    """Печатает заголовок таблицы в консоль."""

    print(
        "| НАЗВАНИЕ ВИДЕО                           | ПРОСМОТРОВ | ЛАЙКОВ | РЕЙТИНГ | ССЫЛКА НА ВИДЕО                               |")


def print_video_info(video_info: dict) -> None:
    """Печатает информацию о видео в консоль в виде строки таблицы."""
    print(
        f"| {video_info['title']:<40} | {video_info['view_count']:<10} | {video_info['like_count']:<6} | {video_info['ratio']:<7} | {video_info['url']:<35} |")


def save_results_to_json(query: str, results: list[dict]) -> None:
    """Сохраняет результаты поиска в файл JSON."""

    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    data = {'query': query, 'timestamp': timestamp, 'results': results}
    with open(SEARCH_RESULTS_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=True, indent=4)


def print_options() -> None:
    """Печатает доступные опции выбора в консоль."""

    print("МЕНЮ:")
    options_str = '\n'.join([f"({key}) {value}" for key, value in OPTIONS.items()])
    print(options_str)
    print("Выберите одну из опций: ", end='')


def main() -> None:
    while True:
        query = input("Введите поисковый запрос: ")
        videos = get_search_results(query)

        for video in videos:
            video.update({'ratio': video['like_count'] / video['view_count']})

        video_stats_sorted = sorted(videos, key=lambda x: x['ratio'], reverse=True)

        print_table_header()
        for i in range(RESULTS_COUNT):
            video_info = format_video_info(video_stats_sorted[i])
            print_video_info(video_info)

        while True:
            print_options()
            choice = input()
            if choice in OPTIONS:
                break
            else:
                print("Выберите одну из доступных опций.")

        if choice == 'n':
            continue
        elif choice == 'w':
            save_results_to_json(query, video_stats_sorted)
            continue
        elif choice == 'wq':
            save_results_to_json(query, video_stats_sorted)
            break
        elif choice == 'q':
            break


if __name__ == '__main__':
    main()
