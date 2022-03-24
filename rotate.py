    def rotate(self, field):
        center = self.blocks[1]
        if not self.rotate_internal(field, center):
            self.rotate_internal(field, self.blocks[2])

    def rotate_internal(self, field, center):
        for block in self.blocks:
            if block.equals(center):
                continue
            
            x = block.x - center.x
            y = block.y - center.y

            newx = x*0 - y*1 + center.x
            newy = x*1 + y*0 + center.y

            if newx >= NUM_COLUMN or newx < 0 or field[newy][newx][0] > -1:
                return False

        for block in self.blocks:
            if block.equals(center):
                continue
            
            x = block.x - center.x
            y = block.y - center.y

            newx = x*0 - y*1 + center.x
            newy = x*1 + y*0 + center.y

            block.x = newx
            block.y = newy

        return True