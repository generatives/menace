function indexToCoord(index) {
    return { x: index % 3, y: parseInt(index / 3) }
}

function createRect(x, y, width, height, colour) {
    const rect = PIXI.Sprite.from(PIXI.Texture.WHITE);
    rect.x = x;
    rect.y = y;
    rect.width = width;
    rect.height = height;
    rect.tint = colour;
    return rect;
}

function GameBoard(stage) {
    const self = this;
    const tileSize = 75;
    const lineWidth = 4

    self.stage = stage
    self.tiles = []
    self.marks = []
    
    for(let i = 0; i < 9; i++) {
        coord = indexToCoord(i)
        const tile = createRect(coord.x * tileSize, coord.y * tileSize, tileSize, tileSize, 0xFFFFFF);
        tile.interactive = true
        tile.pointerdown = function() {
            if(self.tilepressed) {
                self.tilepressed(i)
            }
        }
        
        tile.tint = 0xFFFFFF;

        self.tiles[i] = tile
    }

    self.bars = [
        createRect(tileSize - lineWidth / 2, 0, lineWidth, tileSize * 3, 0x000000),
        createRect(tileSize * 2 - lineWidth / 2, 0, lineWidth, tileSize * 3, 0x000000),
        createRect(0, tileSize - lineWidth / 2, tileSize * 3, lineWidth, 0x000000),
        createRect(0, tileSize * 2 - lineWidth / 2, tileSize * 3, lineWidth, 0x000000)
    ]

    self.setPosition = function(position) {
        for(var mark of this.marks) {
            self.stage.removeChild(mark);
        }

        self.marks = [];
        for(let i = 0; i < 9; i++) {
            const coord = indexToCoord(i);
            const state = position[i];
            if(state == 1) {
                const mark = createRect(coord.x * tileSize + 10, coord.y * tileSize + 10, tileSize - 20, tileSize - 20, 0xFF0000);
                self.stage.addChild(mark);
                self.marks.push(mark);
            }
            if(state == 2) {
                const mark = createRect(coord.x * tileSize + 10, coord.y * tileSize + 10, tileSize - 20, tileSize - 20, 0x00FF00);
                self.stage.addChild(mark);
                self.marks.push(mark);
            }
        }
    }

    for(var tile of self.tiles) {
        self.stage.addChild(tile)
    }
    for(var bar of self.bars) {
        self.stage.addChild(bar)
    }
}