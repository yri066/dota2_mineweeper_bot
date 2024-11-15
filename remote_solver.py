import requests

# URL of the endpoint
url = "https://www.logigames.com/minesweeper/solveboard"

# Headers for the request
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en,ru-RU;q=0.9,ru;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-Type": "text/plain;charset=UTF-8",
    "Host": "www.logigames.com",
    "Origin": "https://www.logigames.com",
    "Pragma": "no-cache",
    "Referer": "https://www.logigames.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}

encoding_mapper = {
    0: (0, 0, 0),
    1: (1, 0, 1),
    2: (2, 0, 1),
    3: (3, 0, 1),
    4: (4, 0, 1),
    5: (5, 0, 1),
    6: (0, 0, 2),
    7: (0, 0, 0),
    8: (0, 0, 0),
    9: (0, 0, 5),
}

# if any action is put on a cell with bonus, it should be put on the top of the list
def sort_actions(actions, board):
    sorted_actions = []
    for action in actions:
        if board[action[1]][action[2]] == 7 or board[action[1]][action[2]] == 8:
            sorted_actions.insert(0, action)
        else:
            sorted_actions.append(action)
    return sorted_actions


def solve_board(board, width, height, n_mines):
    requst_body = [1, width, height, n_mines, 1, 0, 0, 0]
    for row in board:
        for cell in row:
            requst_body.append(encoding_mapper[cell][0])
            requst_body.append(encoding_mapper[cell][1])
            requst_body.append(encoding_mapper[cell][2])

    data = str(requst_body)

    # Sending the POST request
    response = requests.post(url, headers=headers, data=data)

    # Extracting the response
    if response.status_code == 200:
        moves = list(map(int, response.text.strip("[]").split(",")))
        safe_actions = []
        unsafe_actions = []
        for i in range(0, len(moves), 2):
            row = moves[i] // width
            col = moves[i] % width
            if moves[i + 1] == 0:
                safe_actions.append(("click", row, col))
            elif moves[i + 1] == 1:
                safe_actions.append(("flag", row, col))
            elif moves[i + 1] == 2:
                unsafe_actions.append(("guess", row, col))
        if len(safe_actions) > 0:
            return sort_actions(safe_actions, board)
        return [sort_actions(unsafe_actions, board)[0]]
    else:
        raise Exception("Failed to solve the board. Status code: " + str(response.status_code))
