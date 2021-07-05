import qbittorrentapi

state_emojis = {
    'error':              '❌',
    'missingFiles':       '❌',
    'uploading':          '⬆️',
    'pausedUP':           '✅',
    'queuedUP':           '🟡',
    'stalledUP':          '🟡',
    'checkingUP':         '🟡',
    'forcedUP':           '✅',
    'allocating':         '💾',
    'downloading':        '⬇️',
    'metaDL':             '⬇️',
    'pausedDL':           '🟡',
    'queuedDL':           '🟡',
    'stalledDL':          '🟡',
    'checkingDL':         '🟡',
    'forcedDL':           '⬇️',
    'checkingResumeData': '💾',
    'moving':             '💾',
    'unknown':            '❓'
}

state_translations = {
    'error':              'ошибка',
    'missingFiles':       'отсутствуют файлы',
    'uploading':          'раздается',
    'pausedUP':           'загружено',
    'queuedUP':           'в очереди на раздачу',
    'stalledUP':          'в ожидании личеров',
    'checkingUP':         'проверка файлов после загрузки',
    'forcedUP':           '[F] раздается',
    'allocating':         'выделение места',
    'downloading':        'загружается',
    'metaDL':             'загрузка метаданных',
    'pausedDL':           'на паузе',
    'queuedDL':           'в очереди на загрузку',
    'stalledDL':          'в ожидании сидеров',
    'checkingDL':         'проверка файлов в течение загрузки',
    'forcedDL':           '[F] загружается',
    'checkingResumeData': 'стартовая проверка файлов',
    'moving':             'перемещение файлов',
    'unknown':            'неизвестный статус',
}


def get_simple_state_emoji(torrent_data: qbittorrentapi.TorrentDictionary):
    if torrent_data.state_enum.is_checking:
        return '🟡'
    if torrent_data.state_enum.is_complete:
        return '✅'
    if torrent_data.state_enum.is_downloading:
        return '⬇️'
    if torrent_data.state_enum.is_errored:
        return '❌'
    if torrent_data.state_enum.is_paused:
        return '⏸'
    if torrent_data.state_enum.is_uploading:
        return '⬆️'
