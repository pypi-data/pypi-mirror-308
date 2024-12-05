import bs4
import typing
import re
import html

from fitgirl.core.abc import Game, GameData


def get_paragraph(article: bs4.element.Tag, label: str) -> str:
    match = re.search(rf"({label}.*?</strong>)", article.decode(), re.DOTALL)
    if match:
        match_strong = re.search(
            r"<strong>\s*(.*?)\s*</strong>", match.group(1), re.DOTALL
        )
        extracted_text_strong = match_strong.group(1) if match_strong else "N/A"
    else:
        extracted_text_strong = "N/A"
    return extracted_text_strong


def get_screenshots(article: bs4.element.Tag, label: str) -> typing.List[str]:
    # Find the label "Screenshots" and extract all <img> src values following it
    screenshots_section = re.search(rf"{label}.*?</p>", article.decode(), re.DOTALL)
    if screenshots_section:
        # Extract all image src links in the screenshots section
        screenshot_urls = re.findall(
            r'<img[^>]+src="([^"]+)"', screenshots_section.group(0)
        )
        return screenshot_urls
    return []


def get_text(tag: typing.Optional[bs4.element.Tag]) -> str:
    return tag.get_text(strip=True) if tag else "N/A"


def get_attribute(tag: typing.Optional[bs4.element.Tag], attr: str) -> str:
    attribute_value = tag.get(attr, "N/A") if tag else "N/A"
    return (
        " ".join(attribute_value)
        if isinstance(attribute_value, list)
        else attribute_value
    )


def parse_game_data(html: str) -> typing.List[GameData]:
    soup = bs4.BeautifulSoup(html, "html.parser")
    games: typing.List[GameData] = []
    articles = soup.find_all("article", class_="post")

    for article in articles:
        title_tag = article.find("h1", class_="entry-title").find("a")
        title: str = get_text(title_tag)

        date_tag = article.find("time", class_="entry-date")
        date: str = get_attribute(date_tag, "datetime")

        author_tag = article.find("span", class_="author vcard").find("a")
        author: str = get_text(author_tag)

        category_tag = article.find("span", class_="cat-links").find("a")
        category: str = get_text(category_tag)

        details_tag = article.find("div", class_="entry-summary")
        details: str = get_text(details_tag)

        download_links: typing.List[str] = [
            link["href"] for link in details_tag.find_all("a", href=True) if details_tag
        ]

        game_data = GameData(
            title=title,
            date=date,
            author=author,
            category=category,
            details=details,
            download_links=download_links,
        )
        games.append(game_data)

    return games


def get_repack_features(article: bs4.element.Tag, label: str) -> typing.List[str]:
    # Find the "Repack Features" label and extract all <li> text within that section
    repack_features_section = re.search(
        rf"{label}.*?</ul>", article.decode(), re.DOTALL
    )
    if repack_features_section:
        # Extract all <li> content within the repack features section
        features = re.findall(
            r"<li>\s*(.*?)\s*</li>", repack_features_section.group(0), re.DOTALL
        )
        # Clean up any nested tags within <li> elements
        features = [re.sub(r"<[^>]+>", "", feature).strip() for feature in features]
        return [format_repack_features(features[0])]
    return []


def format_repack_features(raw_features: str) -> str:
    # Split the string by newline to process each line separately
    lines = raw_features.strip().splitlines()

    # Strip extra whitespace from each line and unescape HTML entities
    cleaned_lines = [html.unescape(line.strip()) for line in lines if line.strip()]

    # Join lines into a formatted string with bullet points
    formatted_features = "\n".join(f"- {line}" for line in cleaned_lines)

    return formatted_features


def parse_game(html: str) -> typing.List[Game]:
    soup = bs4.BeautifulSoup(html, "html.parser")
    games: typing.List[Game] = []
    articles = soup.find_all("article", class_="post")

    for article in articles:
        title = article.find("h1", class_="entry-title").get_text(strip=True)

        date = article.find("time", class_="entry-date").get("datetime", "N/A")

        author = (
            article.find("span", class_="author vcard").find("a").get_text(strip=True)
        )

        category = (
            article.find("span", class_="cat-links").find("a").get_text(strip=True)
        )

        genres_tags = get_paragraph(article, "Genres/Tags")
        companies = get_paragraph(article, "Companies")
        languages = get_paragraph(article, "Languages")
        original_size = get_paragraph(article, "Original Size")
        repack_size = get_paragraph(article, "Repack Size:")

        screenshots = get_screenshots(article, "Screenshots")
        repack_features = get_repack_features(article, "Repack Features")

        download_links = [
            link["href"]
            for link in article.select("h3:contains('Download Mirrors') + ul li a")
        ]

        games.append(
            Game(
                title=title,
                date=date,
                author=author,
                category=category,
                genres_tags=genres_tags,
                companies=companies,
                languages=languages,
                original_size=original_size,
                repack_size=repack_size,
                download_links=download_links,
                screenshots=screenshots,
                repack_features=repack_features,  # Add repack_features field to Game if needed
            )
        )

    return games
