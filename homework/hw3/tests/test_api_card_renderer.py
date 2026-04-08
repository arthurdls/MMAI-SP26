import pytest
from PIL import ImageFont

# ---------- helpers ----------
FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    "/usr/share/fonts/truetype/liberation/LiberationMono-Regular.ttf",
    "/usr/share/fonts/truetype/ubuntu/UbuntuMono-R.ttf",
    "/usr/share/fonts/truetype/freefont/FreeMono.ttf",
]

def test_load_font_returns_truetype_or_default():
    from api_card_renderer import load_font
    fnt = load_font(12)
    assert fnt is not None
    assert hasattr(fnt, "getbbox") or hasattr(fnt, "getsize")

# ---------- clean_description ----------

def test_clean_description_extracts_inner_quoted_text():
    from api_card_renderer import clean_description
    raw = 'This is the subfunction for tool "instagram_cheapest", you can use this tool.' \
          'The description of this function is: "get userinfo by username"'
    assert clean_description(raw) == "get userinfo by username"

def test_clean_description_single_quotes():
    from api_card_renderer import clean_description
    raw = "The description of this function is: 'find breweries by city'"
    assert clean_description(raw) == "find breweries by city"

def test_clean_description_boilerplate_only_returns_subfunction_of():
    from api_card_renderer import clean_description
    raw = 'This is the subfunction for tool "languagetool", you can use this tool.'
    result = clean_description(raw)
    assert result == "(subfunction of languagetool)"

def test_clean_description_empty_string():
    from api_card_renderer import clean_description
    assert clean_description("") == "(no description)"

def test_clean_description_no_pattern_match():
    from api_card_renderer import clean_description
    assert clean_description("Random unrecognised text") == "(no description)"

def test_clean_description_truncates_at_90_chars():
    from api_card_renderer import clean_description
    long_inner = "A" * 100
    raw = f'The description of this function is: "{long_inner}"'
    result = clean_description(raw)
    assert len(result) <= 93
    assert result.endswith("…")

# ---------- get_param_pills ----------

def test_get_param_pills_required_and_optional():
    from api_card_renderer import get_param_pills
    params = {
        "type": "object",
        "required": ["username"],
        "optional": ["limit"],
        "properties": {
            "username": {"type": "STRING", "description": ""},
            "limit":    {"type": "INTEGER", "description": ""},
        },
    }
    req, opt = get_param_pills(params)
    assert req == [("username", "string")]
    assert opt == [("limit", "integer")]

def test_get_param_pills_empty_properties():
    from api_card_renderer import get_param_pills
    params = {"type": "object", "required": [], "optional": [], "properties": {}}
    req, opt = get_param_pills(params)
    assert req == []
    assert opt == []

def test_get_param_pills_missing_type_falls_back_to_any():
    from api_card_renderer import get_param_pills
    params = {
        "type": "object",
        "required": ["q"],
        "optional": [],
        "properties": {"q": {"description": "search query"}},
    }
    req, opt = get_param_pills(params)
    assert req == [("q", "any")]
    assert opt == []

def test_get_param_pills_caps_at_six_total():
    from api_card_renderer import get_param_pills
    props = {f"p{i}": {"type": "STRING"} for i in range(10)}
    params = {
        "type": "object",
        "required": [f"p{i}" for i in range(5)],
        "optional": [f"p{i}" for i in range(5, 10)],
        "properties": props,
    }
    req, opt = get_param_pills(params)
    assert len(req) + len(opt) <= 6

def test_get_param_pills_none_params():
    from api_card_renderer import get_param_pills
    req, opt = get_param_pills(None)
    assert req == []
    assert opt == []

# ---------- render_one_example ----------
import json
import tempfile
from pathlib import Path
from PIL import Image

def _make_row(apis: list[dict]) -> dict:
    """Build a minimal DataFrame-row-like dict for testing."""
    return {"api_list_json": json.dumps(apis)}

def test_render_creates_jpg_file():
    from api_card_renderer import render_one_example
    apis = [{"name": "test_api", "description": "A test API.",
             "parameters": {"type": "object", "required": [], "optional": [], "properties": {}}}]
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "test.jpg"
        render_one_example(_make_row(apis), out)
        assert out.exists()
        assert out.stat().st_size > 0

def test_render_output_is_valid_jpeg():
    from api_card_renderer import render_one_example
    apis = [{"name": "my_api", "description": "Does things.",
             "parameters": {"type": "object", "required": ["q"], "optional": [],
                            "properties": {"q": {"type": "STRING"}}}}]
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "out.jpg"
        render_one_example(_make_row(apis), out)
        img = Image.open(out)
        assert img.format == "JPEG"

def test_render_canvas_width_is_800():
    from api_card_renderer import render_one_example
    apis = [{"name": "api_one", "description": "desc",
             "parameters": {"type": "object", "required": [], "optional": [], "properties": {}}}]
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "out.jpg"
        render_one_example(_make_row(apis), out)
        img = Image.open(out)
        assert img.size[0] == 800

def test_render_canvas_height_minimum_is_900():
    from api_card_renderer import render_one_example
    apis = [{"name": "only_one", "description": "single api",
             "parameters": {"type": "object", "required": [], "optional": [], "properties": {}}}]
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "out.jpg"
        render_one_example(_make_row(apis), out)
        img = Image.open(out)
        assert img.size[1] >= 900

def test_render_canvas_height_scales_with_api_count():
    from api_card_renderer import render_one_example
    def _api(name):
        return {"name": name, "description": "desc",
                "parameters": {"type": "object", "required": [], "optional": [], "properties": {}}}
    apis_2 = [_api("a"), _api("b")]
    apis_10 = [_api(f"api_{i}") for i in range(10)]
    with tempfile.TemporaryDirectory() as tmp:
        out2  = Path(tmp) / "two.jpg"
        out10 = Path(tmp) / "ten.jpg"
        render_one_example(_make_row(apis_2),  out2)
        render_one_example(_make_row(apis_10), out10)
        h2  = Image.open(out2).size[1]
        h10 = Image.open(out10).size[1]
        assert h10 > h2

def test_render_empty_api_list_shows_placeholder():
    from api_card_renderer import render_one_example
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "empty.jpg"
        render_one_example(_make_row([]), out)
        assert out.exists()  # should not crash

def test_render_15_apis_stays_portrait():
    from api_card_renderer import render_one_example
    def _api(name):
        return {"name": name, "description": "desc",
                "parameters": {"type": "object", "required": [], "optional": [], "properties": {}}}
    apis = [_api(f"api_{i}") for i in range(15)]
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "fifteen.jpg"
        render_one_example(_make_row(apis), out)
        img = Image.open(out)
        w, h = img.size
        assert h > w  # must be portrait

def test_render_long_api_name_does_not_crash():
    """API names > 60 chars must be truncated without error (spec §Edge Cases)."""
    from api_card_renderer import render_one_example
    apis = [{"name": "a" * 80, "description": "long name api",
             "parameters": {"type": "object", "required": [], "optional": [], "properties": {}}}]
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "longname.jpg"
        render_one_example(_make_row(apis), out)
        assert out.exists()

def test_render_overflow_params_does_not_crash():
    """> 6 params must show +N more label without crashing (spec §Edge Cases)."""
    from api_card_renderer import render_one_example
    props = {f"p{i}": {"type": "STRING"} for i in range(10)}
    apis = [{"name": "many_params", "description": "has lots of params",
             "parameters": {
                 "type": "object",
                 "required": [f"p{i}" for i in range(5)],
                 "optional": [f"p{i}" for i in range(5, 10)],
                 "properties": props,
             }}]
    with tempfile.TemporaryDirectory() as tmp:
        out = Path(tmp) / "overflow.jpg"
        render_one_example(_make_row(apis), out)
        assert out.exists()

# ---------- truncate_text ----------

def test_truncate_text_short_string_unchanged():
    from api_card_renderer import truncate_text
    assert truncate_text("hello", 20) == "hello"

def test_truncate_text_exact_length_unchanged():
    from api_card_renderer import truncate_text
    s = "A" * 10
    assert truncate_text(s, 10) == s

def test_truncate_text_long_string_truncated_with_ellipsis():
    from api_card_renderer import truncate_text
    s = "A" * 50
    result = truncate_text(s, 30)
    assert len(result) <= 33  # 30 + "..."
    assert result.endswith("...")

def test_truncate_text_none_returns_empty():
    from api_card_renderer import truncate_text
    assert truncate_text(None, 100) == ""

def test_truncate_text_pipe_separated_string():
    """Validates that function_calls_used (pipe-separated) is handled as plain text."""
    from api_card_renderer import truncate_text
    s = "search_breweries|get_brewery_by_id|autocomplete"
    result = truncate_text(s, 300)
    assert result == s  # no truncation needed under 300
