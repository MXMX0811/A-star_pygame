import pygame
from pygame.locals import *
from sys import exit


N = 20
wall = [0 for i in range(400)]
start = 1000
end = 1000


class Node(object):
    def __init__(self, x, y, g=0, p=None):
        self.coordinate_x = x
        self.coordinate_y = y
        self.val_g = g
        self.pre = p
        self.val = self.function_f()

    def function_h(self):
        return abs(self.coordinate_x - end % 20) + abs(self.coordinate_y - end // 20)

    def function_f(self):
        return self.function_h() + self.val_g


def clear_pic(x, y):
    pygame.draw.rect(screen, [145, 145, 145], [15 + x * 30, 15 + y * 30, 30, 30], 1)
    pygame.draw.rect(screen, [255, 255, 255], [16 + x * 30, 16 + y * 30, 28, 28], 0)
    pygame.display.flip()


pygame.init()
screen_caption = pygame.display.set_caption('A star')
screen = pygame.display.set_mode([630, 630])
screen.fill([255, 255, 255])
gameIcon = pygame.image.load("icon.png")
pygame.display.set_icon(gameIcon)
mouse_x, mouse_y = 0, 0
open = []
closed = []
x0 = 0
y0 = 0
pygame.draw.rect(screen, [145, 145, 145], [14, 14, 602, 602], 1)
for i in range(N):
    for j in range(N):
        pygame.draw.rect(screen, [145, 145, 145], [15 + i * 30, 15 + j * 30, 30, 30], 1)
pygame.display.flip()
while 1:
    for event in pygame.event.get():
        if_event = 0
        if event.type == QUIT:
            exit()
        elif event.type == MOUSEBUTTONDOWN:
            if_event = 1
            pressed_array = pygame.mouse.get_pressed()
            for index in range(len(pressed_array)):
                if pressed_array[index]:
                    if index == 0:
                        print('Pressed LEFT Button!')
                        pos = pygame.mouse.get_pos()
                        mouse_x = pos[0]
                        mouse_y = pos[1]
                        i = (mouse_x - 15) // 30
                        j = (mouse_y - 15) // 30
                        n = 20 * j + i
                        if 15 <= mouse_x <= 615 and 15 <= mouse_y <= 615 and n != start and n != end:
                            if wall[n] == 0:
                                wall[n] = 1
                                pic = pygame.image.load("wall.jpg")
                                position = pic.get_rect()
                                position = (16 + i * 30, 16 + j * 30)
                                screen.blit(pic, position)
                                pygame.display.flip()
                                print("横：", i, " 纵：", j, " 第", n, "个：", wall[n])

                            elif wall[n] == 1:
                                wall[n] = 0
                                clear_pic(i, j)
                                print("横：", i, " 纵：", j, " 第", n, "个：", wall[n])

                    elif index == 1:
                        print('The mouse wheel Pressed!')
                        pos = pygame.mouse.get_pos()
                        mouse_x = pos[0]
                        mouse_y = pos[1]
                        i = (mouse_x - 15) // 30
                        j = (mouse_y - 15) // 30
                        n = 20 * j + i
                        if 15 <= mouse_x <= 615 and 15 <= mouse_y <= 615 and wall[n] != 1 and n != start:
                            i = end % 20
                            j = end // 20
                            clear_pic(i, j)
                            i = (mouse_x - 15) // 30
                            j = (mouse_y - 15) // 30
                            n = 20 * j + i
                            end = n
                            pic = pygame.image.load("zhongdian.jpg")
                            position = pic.get_rect()
                            position = (16 + i * 30, 16 + j * 30)
                            screen.blit(pic, position)
                            pygame.display.flip()
                            print("横：", i, " 纵：", j, " 第", n, "个为终点")
                    elif index == 2:
                        print('Pressed RIGHT Button!')
                        pos = pygame.mouse.get_pos()
                        mouse_x = pos[0]
                        mouse_y = pos[1]
                        i = (mouse_x - 15) // 30
                        j = (mouse_y - 15) // 30
                        n = 20 * j + i
                        if 15 <= mouse_x <= 615 and 15 <= mouse_y <= 615 and wall[n] != 1 and n != end:
                            i = start % 20
                            j = start // 20
                            clear_pic(i, j)
                            i = (mouse_x - 15) // 30
                            j = (mouse_y - 15) // 30
                            n = 20 * j + i
                            start = n
                            pic = pygame.image.load("qidian.jpg")
                            position = pic.get_rect()
                            position = (16 + i * 30, 16 + j * 30)
                            screen.blit(pic, position)
                            pygame.display.flip()
                            print("横：", i, " 纵：", j, " 第", n, "个为起点")

        if start != 1000 and end != 1000 and if_event == 1:       # 有起点和终点且进行过操作需要重新计算
            open = []
            closed = []
            curr = None
            for i in range(20):
                for j in range(20):
                    if wall[j * 20 + i] == 0 and j * 20 + i != start and j * 20 + i != end:
                        clear_pic(i, j)

            starting_point = Node(start % 20, start // 20, 0)      # 为起点新建结点并将其加入open表
            open.append(starting_point)

            while 1:
                if len(open) == 0:
                    print("未找到路径！")
                    break

                if curr:
                    if curr.coordinate_x + curr.coordinate_y * 20 == start:
                        clear_pic(curr.coordinate_x, curr.coordinate_y)
                        pic = pygame.image.load("qidian.jpg")
                        position = pic.get_rect()
                        position = (16 + curr.coordinate_x * 30, 16 + curr.coordinate_y * 30)
                        screen.blit(pic, position)
                        pygame.display.flip()
                    else:
                        clear_pic(curr.coordinate_x, curr.coordinate_y)
                best = 0
                for i in range(len(open)):      # 从open表中选择估价最低的结点
                    if open[i].val <= open[best].val:
                        best = i

                if open[best].coordinate_x + open[best].coordinate_y * 20 == end:       # 如果该节点是终点
                    print("已找到路径！")
                    curr = open[best]
                    while curr.pre:
                        print(curr.coordinate_x + curr.coordinate_y * 20)
                        if curr.coordinate_x + curr.coordinate_y * 20 != end:
                            pygame.draw.rect(screen, [255, 255, 0],
                                             [16 + curr.coordinate_x * 30, 16 + curr.coordinate_y * 30, 28, 28], 0)
                        pygame.display.flip()
                        curr = curr.pre
                    break
                curr = open[best]
                closed.append(open[best])  # 将best结点移入closed表
                open.pop(best)

                # 扩展best周围可通过结点
                if curr.coordinate_x + 1 < 20 \
                        and wall[curr.coordinate_x + 1 + curr.coordinate_y * 20] == 0:
                    flag = 0  # 用以标记是否在表中
                    i = 0
                    while 1:
                        if i >= len(open):
                            break
                        if curr.coordinate_x + 1 == open[i].coordinate_x \
                                and curr.coordinate_y == open[i].coordinate_y:        # 该节点已存在open表中
                            flag = 1  # 标记
                            if open[i].val_g >= curr.val_g + 1:        # 如果新的估价更低
                                open[i].pre = curr
                                open[i].val_g = curr.val_g + 1
                                open[i].val = open[i].function_f()
                                break
                        i += 1

                    i = 0
                    while 1:
                        if i >= len(closed):
                            break
                        if curr.coordinate_x + 1 == closed[i].coordinate_x \
                                and curr.coordinate_y == closed[i].coordinate_y:        # 该节点已存在closed表中
                            flag = 1  # 标记
                            if closed[i].val_g >= curr.val_g + 1:        # 如果估价低于best结点
                                closed[i].pre = curr
                                closed[i].val_g = curr.val_g + 1
                                closed[i].val = closed[i].function_f()
                                open.append(closed[i])
                                closed.pop(i)
                                break
                        i += 1

                    if flag == 0:       # 若不存在将其加入open表
                        new_point = Node(curr.coordinate_x + 1, curr.coordinate_y, curr.val_g + 1, curr)
                        open.append(new_point)

                if curr.coordinate_x - 1 >= 0 \
                        and wall[curr.coordinate_x - 1 + curr.coordinate_y * 20] == 0:
                    flag = 0  # 用以标记是否在表中
                    i = 0
                    while 1:
                        if i >= len(open):
                            break
                        if curr.coordinate_x - 1 == open[i].coordinate_x \
                                and curr.coordinate_y == open[i].coordinate_y:
                            flag = 1  # 标记
                            if open[i].val_g >= curr.val_g + 1:        # 如果新的估价更低
                                open[i].pre = curr
                                open[i].val_g = curr.val_g + 1
                                open[i].val = open[i].function_f()
                                break
                        i += 1

                    i = 0
                    while 1:
                        if i >= len(closed):
                            break
                        if curr.coordinate_x - 1 == closed[i].coordinate_x \
                                and curr.coordinate_y == closed[i].coordinate_y:
                            flag = 1  # 标记
                            if closed[i].val_g >= curr.val_g + 1:        # 如果估价低于best结点
                                closed[i].pre = curr
                                closed[i].val_g = curr.val_g + 1
                                closed[i].val = closed[i].function_f()
                                open.append(closed[i])
                                closed.pop(i)
                                break
                        i += 1
                    if flag == 0:
                        new_point = Node(curr.coordinate_x - 1, curr.coordinate_y, curr.val_g + 1, curr)
                        open.append(new_point)

                if curr.coordinate_y + 1 < 20 \
                        and wall[curr.coordinate_x + (curr.coordinate_y + 1) * 20] == 0:
                    flag = 0  # 用以标记是否在表中
                    i = 0
                    while 1:
                        if i >= len(open):
                            break
                        if curr.coordinate_x == open[i].coordinate_x \
                                and curr.coordinate_y + 1 == open[i].coordinate_y:
                            flag = 1  # 标记
                            if open[i].val_g >= curr.val_g + 1:        # 如果新的估价更低
                                open[i].pre = curr
                                open[i].val_g = curr.val_g + 1
                                open[i].val = open[i].function_f()
                                break
                        i += 1

                    i = 0
                    while 1:
                        if i >= len(closed):
                            break
                        if curr.coordinate_x == closed[i].coordinate_x \
                                and curr.coordinate_y + 1 == closed[i].coordinate_y:
                            flag = 1  # 标记
                            if closed[i].val_g >= curr.val_g + 1:        # 如果估价低于best结点
                                closed[i].pre = curr
                                closed[i].val_g = curr.val_g + 1
                                closed[i].val = closed[i].function_f()
                                open.append(closed[i])
                                closed.pop(i)
                                break
                        i += 1
                    if flag == 0:
                        new_point = Node(curr.coordinate_x, curr.coordinate_y + 1, curr.val_g + 1, curr)
                        open.append(new_point)

                if curr.coordinate_y - 1 >= 0 \
                        and wall[curr.coordinate_x + (curr.coordinate_y - 1) * 20] == 0:
                    flag = 0  # 用以标记是否在表中
                    i = 0
                    while 1:
                        if i >= len(open):
                            break
                        if curr.coordinate_x == open[i].coordinate_x \
                                and curr.coordinate_y - 1 == open[i].coordinate_y:
                            flag = 1  # 标记
                            if open[i].val_g >= curr.val_g + 1:        # 如果新的估价更低
                                open[i].pre = curr
                                open[i].val_g = curr.val_g + 1
                                open[i].val = open[i].function_f()
                                break
                        i += 1

                    i = 0
                    while 1:
                        if i >= len(closed):
                            break
                        if curr.coordinate_x == closed[i].coordinate_x \
                                and curr.coordinate_y - 1 == closed[i].coordinate_y:
                            flag = 1  # 标记
                            if closed[i].val_g >= curr.val_g + 1:        # 如果估价低于best结点
                                closed[i].pre = curr
                                closed[i].val_g = curr.val_g + 1
                                closed[i].val = closed[i].function_f()
                                open.append(closed[i])
                                closed.pop(i)
                                break
                        i += 1
                    if flag == 0:
                        new_point = Node(curr.coordinate_x, curr.coordinate_y - 1, curr.val_g + 1, curr)
                        open.append(new_point)
                for i in range(len(open)):
                    if open[i].coordinate_x + open[i].coordinate_y * 20 != start \
                            and open[i].coordinate_x + open[i].coordinate_y * 20 != end:
                        pygame.draw.rect(screen, [154, 255, 154], [16 + open[i].coordinate_x * 30,
                                                               16 + open[i].coordinate_y * 30, 28, 28], 0)
                for i in range(len(closed)):
                    if closed[i].coordinate_x + closed[i].coordinate_y * 20 != start\
                            and closed[i].coordinate_x + closed[i].coordinate_y * 20 != end:
                        pygame.draw.rect(screen, [0, 235, 220], [16 + closed[i].coordinate_x * 30,
                                                               16 + closed[i].coordinate_y * 30, 28, 28], 0)

                pygame.draw.rect(screen, [255, 0, 0], [16 + curr.coordinate_x * 30, 16 + curr.coordinate_y * 30, 28, 28], 0)
                pygame.display.flip()