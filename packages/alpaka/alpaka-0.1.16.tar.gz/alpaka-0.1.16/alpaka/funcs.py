from .vars import get_current_alpaka
from koil import unkoil


async def achat(*args, **kwargs):
    alpaka = get_current_alpaka()
    return await alpaka.chat(*args, **kwargs)


def chat(*args, **kwargs):
    return unkoil(achat, *args, **kwargs)


async def apull(*args, **kwargs):
    alpaka = get_current_alpaka()
    print(args, kwargs)
    return await alpaka.pull(*args, **kwargs)


def pull(*args, **kwargs):
    return unkoil(apull, *args, **kwargs)
