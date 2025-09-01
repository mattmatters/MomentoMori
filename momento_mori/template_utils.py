"""Template utilities and filters for Jinja2."""


def get_death_image_for_years(years_remaining: float) -> str:
    """Select appropriate death imagery based on remaining life expectancy.

    This is presentation logic that determines which image to show
    based on the calculated years remaining.
    """
    if years_remaining > 50:
        return "time-gentle.svg"
    elif years_remaining > 20:
        return "death-mild.jpg"
    elif years_remaining > 5:
        return "death-moderate.jpg"
    else:
        return "death-severe.jpg"


def register_template_filters(templates):
    """Register custom template filters with Jinja2."""
    templates.env.filters["death_image"] = get_death_image_for_years
    return templates
