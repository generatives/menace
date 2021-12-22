function TicTacToeApp(stage) {
    const self = this;

    self.stage = stage;
    self.gameBoard = new GameBoard(stage);
    self.position = [0, 0, 0, 0, 0, 0, 0, 0, 0];
    self.opponent = 0;

    self.renderNextTurn = function(turns) {
        turn = turns.shift();
        self.position = turn.position
        self.gameBoard.setPosition(turn.position)
        if(turns.length) {
            setTimeout(() => self.renderNextTurn(turns), 200)
        }
    }

    self.makeMove = function (move) {
        const requestParams = {
            position: self.position,
            move,
            opponent: self.opponent
        }
        fetch("/move", {
            method: "POST",
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestParams)
        })
        .then(response => response.json())
        .then(function(result) {
            if(result.turns.length) {
                self.renderNextTurn(result.turns)
            }
        })
    }

    self.restartGame = function() {
        self.position = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.gameBoard.setPosition(self.position)
        self.makeMove(null)
    }

    self.setOpponent = function(opponent) {
        self.opponent = opponent
    }

    self.gameBoard.tilepressed = self.makeMove;
}