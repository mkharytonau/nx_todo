from colored import bg, fg, attr


def colorize(data, background=None, foreground=None):
    if background and foreground:
        return '{bg}{fg}{data}{ce}'.format(bg=bg(background), fg=fg(foreground),
                                       data=data, ce=attr('reset'))
    if not background and foreground:
        return '{fg}{data}{ce}'.format(fg=fg(foreground), data=data, ce=attr('reset'))
    if background and not foreground:
        return '{bg}{data}{ce}'.format(bg=bg(background), data=data, ce=attr('reset'))
    return data