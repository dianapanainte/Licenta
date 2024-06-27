from django import template

register = template.Library()


@register.filter
def percentage(wins, losses):
    wins = int(wins)
    losses = int(losses)
    if wins + losses == 0:
        return 0
    return round((wins / (wins + losses)) * 100, 2)
