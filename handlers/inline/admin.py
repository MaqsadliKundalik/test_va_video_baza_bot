from aiogram import Router, types, F
from database.models import Test, Category, VideoLessons
from keyboards.admin import test_actions_markup

router = Router()

@router.inline_query(F.query.startswith("cat_"))
async def inline_test_query(query: types.InlineQuery):
    try:
        parts = query.query.split("_")
        category_id = int(parts[1])
    except (ValueError, IndexError):
        return

    tests = await Test.filter(category_id=category_id).all()
    print(tests)
    results = []
    for test in tests:
        # Check if video exists for this test
        video = await VideoLessons.get_or_none(test_id=test.id)
        has_video = video is not None
        
        results.append(
            types.InlineQueryResultArticle(
                id=str(test.id),
                title=test.name,
                input_message_content=types.InputTextMessageContent(
                    message_text=f"/manage_test_{test.id}"
                )
            )
        )
    if results:
        await query.answer(results, cache_time=1, is_personal=True)
    else:
        await query.answer(
            results=[types.InlineQueryResultArticle(
                id="no_results",
                title="Testlar mavjud emas",
                input_message_content=types.InputTextMessageContent(
                    message_text="Testlar mavjud emas"
                )
            )],
            cache_time=1, is_personal=True
        )
