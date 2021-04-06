from pytest import  fixture
from app.models.color_model import ColorModel

@fixture
def color_model() -> ColorModel:
    return ColorModel(
        color_id = 1, 
        color_value = 'FFFFFF'
    )

def test_ColorModel_create(color_model: ColorModel):
    assert  color_model