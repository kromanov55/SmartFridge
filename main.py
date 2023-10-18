import base64
import requests
import streamlit as st
from ultralytics import YOLO
import os
from translate import Translator
import shutil
import openai
import streamlit_antd_components as sac
import re
import io
from PIL import Image

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.content

openai.api_key = "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"
translator= Translator(to_lang="Russian")
translator_1= Translator(to_lang="en")

def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

def order():

    st.title("Вы успешно совершили заказ!")
    st.divider()
    st.subheader("Ваш курьер уже в пути!")
    st.subheader("Приблизительное время доставки:")
    st.subheader("15:44")
    st.balloons()

def bin_approvement():
    st.title("Утверждение корзины")
    st.subheader("Список продуктов к заказу:")
    st.markdown("Чтобы убрать продукт из корзины, нажмите ❌")
    st.text("Яйца, 110 рублей")
    col11, col22 = st.columns([1, 1])
    with col11:
        st.image('eggs.jpg', width=300)
    with col22:
        st.text('❌')
    st.text("Курица, 410 рублей")
    col12, col222 = st.columns([1, 1])
    with col12:
        st.image('chicken.jpg', width=300)
    with col222:
        st.text('❌')
    st.text("Гречка, 75 рублей")
    col12, col222 = st.columns([1, 1])
    with col12:
        st.image('grechkrupa.png', width=300)
    with col222:
        st.text('❌')
def registration():
    st.title('Регистрация')
    fname = st.text_input('Имя:')
    lname = st.text_input('Фамилия:')
    email = st.text_input('Почта:')
    gender = st.radio('Пол', ('Мужской', 'Женский'))
    age = st.slider('Возраст:', 1, 120)
    bday = st.date_input('Дата рождения:')
    submit = st.button('Зарегистрироваться')
    if submit:
        st.text("После регистрации можете перейти к следующему разделу интерфейса")


    # col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 1, 1, 1, 1])
    # with col1:
    #     st.button('ПН')
    # with col2:
    #     st.button('ВТ')
    # with col3:
    #     st.button('СР')
    # with col4:
    #     st.button('ЧТ')
    # with col5:
    #     st.button('ПТ')
    # with col6:
    #     st.button('СБ')
    # with col7:
    #     st.button('ВС')
    # st.subheader('Завтрак: яичница на помидорах')
    # st.image('breakfast.jpg', width=550)
    # st.success('Имеющиеся продукты: помидоры')
    # st.error('Необходимо заказать: яйца')
    # st.subheader('Обед: чечевичный крем-суп')
    # st.image('lunch.jpg', width=550)
    # st.error('Необходимо заказать: чечевица, лимон')
    # st.subheader('Ужин: гречка по-купечески')
    # st.image('dinner.jpg', width=550)
    # st.success('Имеющиеся продукты: помидоры черри')
    # st.error('Необходимо заказать: курица, гречневая крупа, морковь')

def main_page():
    food_list = ""
    model = YOLO("best.pt")
    nav = sac.steps(
        items=[
            sac.StepsItem(title='step 1', subtitle='Выбор продуктов', description='''Выберите продукты'''),
            sac.StepsItem(title='step 2', subtitle='Подбор блюд', description='''ИИ подберёт для вас рецепты'''),
            sac.StepsItem(title='step 3', subtitle='Корзина', description='''Корзина для заказа!'''),
            sac.StepsItem(title='step 4', subtitle='Заказ', description='Заказ успешно совершён!'),
        ], format_func='title', placement='vertical', type='navigation', index=0
    )
    a = sac.buttons([
        sac.ButtonsItem(label='Отсканировать продукты при помощи ИИ', color='#2C30BD'),
        sac.ButtonsItem(label='Внести продукты вручную', color='#2C30BD'),
    ], format_func=None, align='center', size='middle', shape='round', type='primary')
    if a == 'Отсканировать продукты при помощи ИИ':
        st.subheader("Приложите в поле ниже фотографии блюд в вашем холодильнике")
        lst = []
        uploaded_files = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"],
                                          accept_multiple_files=True)
        if uploaded_files is not None:
            for uploaded_file in uploaded_files:
                with open(os.path.join("tempDir", uploaded_file.name), "wb") as f:
                    f.write(uploaded_file.getbuffer())
                n = f"tempDir/{uploaded_file.name}"
                results = model.predict(source=n, conf=0.2, save=True)  # save plotted images

                for result in results:
                    if result.boxes:
                        box = result.boxes[0]
                        class_id = int(box.cls)
                        object_name = model.names[class_id]
                        lst.append(object_name)

                l = list(os.listdir('runs/detect'))
                last = l[-1]
                path = f'runs/detect/{last}/{uploaded_file.name}'
                st.image(path, width=550)
            st.subheader("В холодильнике есть:")
            food_str = ""
            count = 0
            for i in lst:
                count += 1
                translation = translator.translate(i)
                food_str += translation
                food_str += " "
                food = f'Продукт {count}: {translation}'
                st.markdown(food)
            st.markdown(
                "Если какие либо продукты остались нераспознанны или вы хотите их добавить, впишите их ниже")
            food_input = st.text_input(
                "Внесите в список оставшиеся продукты без запятой в формате: томаты огурцы картофель")
            button_food = st.button("Нажмите, чтобы добавить продукты в список")
            if button_food:
                food_str += " "
                food_str += food_input
                st.markdown("Новый список:")
                st.markdown(food_str)
                food_list = food_str
            button_to_gpt = st.button("Нажмите здесь, чтобы перейти к подбору меню")
            # shutil.rmtree('runs')
    elif a == 'Внести продукты вручную':
        g = st.button('llll')
        if g:
            del nav
            st.markdown(nav.title())
            nav = sac.steps(
                items=[
                    sac.StepsItem(title='step 1', subtitle='Выбор продуктов', description='''Выберите продукты'''),
                    sac.StepsItem(title='step 2', subtitle='Подбор блюд',
                                  description='''ИИ подберёт для вас рецепты'''),
                    sac.StepsItem(title='step 3', subtitle='Корзина', description='''Корзина для заказа!'''),
                    sac.StepsItem(title='step 4', subtitle='Заказ', description='Заказ успешно совершён!'),
                ], index=1, format_func='title', placement='vertical', type='navigation'
            )
        food_str = ""
        food_input = st.text_input(
            "Внесите в список оставшиеся продукты без запятой в формате: томаты огурцы картофель")
        button_food = st.button("Нажмите, чтобы добавить продукты в список")
        if button_food:
            food_str += food_input
            st.markdown(food_str)
        button_to_gpt = st.button("Нажмите здесь, чтобы перейти к подбору меню")
        if button_to_gpt:
            file = open('myfile.txt', 'w')
            file.write("New content for the file")
            file.close()
            # shutil.rmtree('runs')


def nextpage(): st.session_state.page += 1
def restart(): st.session_state.page = 0
def main():
    st.set_page_config(layout="wide")
    if "page" not in st.session_state:
        st.session_state.page = 0
    st.header("Умный ассистент для холодильника")

    placeholder = st.empty()
    st.button("Next", on_click=nextpage, disabled=(st.session_state.page > 3))

    if st.session_state.page == 0:
        food_list = ""
        model = YOLO("best.pt")
        nav = sac.steps(
            items=[
                sac.StepsItem(title='step 1', subtitle='Выбор продуктов', description='''Выберите продукты'''),
                sac.StepsItem(title='step 2', subtitle='Подбор блюд', description='''ИИ подберёт для вас рецепты'''),
                sac.StepsItem(title='step 3', subtitle='Корзина', description='''Корзина для заказа!'''),
                sac.StepsItem(title='step 4', subtitle='Заказ', description='Заказ успешно совершён!'),
            ], format_func='title', placement='vertical', type='navigation', index=0
        )
        a = sac.buttons([
            sac.ButtonsItem(label='Отсканировать продукты при помощи ИИ', color='#2C30BD'),
            sac.ButtonsItem(label='Внести продукты вручную', color='#2C30BD'),
        ], format_func=None, align='center', size='middle', shape='round', type='primary')
        if a == 'Отсканировать продукты при помощи ИИ':
            st.subheader("Приложите в поле ниже фотографии блюд в вашем холодильнике")
            lst = []
            uploaded_files = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"],
                                              accept_multiple_files=True)
            if uploaded_files is not None:
                for uploaded_file in uploaded_files:
                    with open(os.path.join("tempDir", uploaded_file.name), "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    n = f"tempDir/{uploaded_file.name}"
                    results = model.predict(source=n, conf=0.2, save=True)  # save plotted images

                    for result in results:
                        if result.boxes:
                            box = result.boxes[0]
                            class_id = int(box.cls)
                            object_name = model.names[class_id]
                            lst.append(object_name)

                    l = list(os.listdir('runs/detect'))
                    last = l[-1]
                    path = f'runs/detect/{last}/{uploaded_file.name}'
                    st.image(path, width=550)
                st.subheader("В холодильнике есть:")
                food_str = ""
                count = 0
                for i in lst:
                    count += 1
                    translation = translator.translate(i)
                    food_str += translation
                    food_str += " "
                    food = f'Продукт {count}: {translation}'
                    st.markdown(food)
                st.markdown(
                    "Если какие либо продукты остались нераспознанны или вы хотите их добавить, впишите их ниже")
                food_input = st.text_input(
                    "Внесите в список оставшиеся продукты без запятой в формате: томаты огурцы картофель")
                button_food = st.button("Нажмите, чтобы добавить продукты в список")
                if button_food:
                    food_str += " "
                    food_str += food_input
                    st.markdown("Новый список:")
                    st.markdown(food_str)
                    food_list = food_str
                # shutil.rmtree('runs')
                file = open('myfile.txt', 'w')
                file.write(food_str)
                file.close()
                button_to_gpt = st.button("Нажмите здесь, чтобы перейти к подбору меню", on_click=nextpage,
                                          disabled=(st.session_state.page > 3))
                if button_to_gpt:
                    nextpage()
        elif a == 'Внести продукты вручную':
            g = st.button('llll')
            if g:
                del nav
                st.markdown(nav.title())
                nav = sac.steps(
                    items=[
                        sac.StepsItem(title='step 1', subtitle='Выбор продуктов', description='''Выберите продукты'''),
                        sac.StepsItem(title='step 2', subtitle='Подбор блюд',
                                      description='''ИИ подберёт для вас рецепты'''),
                        sac.StepsItem(title='step 3', subtitle='Корзина', description='''Корзина для заказа!'''),
                        sac.StepsItem(title='step 4', subtitle='Заказ', description='Заказ успешно совершён!'),
                    ], index=1, format_func='title', placement='vertical', type='navigation'
                )
            food_str = ""
            food_input = st.text_input(
                "Внесите в список оставшиеся продукты без запятой в формате: томаты огурцы картофель")
            button_food = st.button("Нажмите, чтобы добавить продукты в список")
            if button_food:
                food_str += food_input
                st.markdown(food_str)
            button_to_gpt = st.button("Нажмите здесь, чтобы перейти к подбору меню", on_click=nextpage, disabled=(st.session_state.page > 3))
            if button_to_gpt:
                file = open('myfile.txt', 'w')
                file.write("New content for the file")
                file.close()
                nextpage()
                # shutil.rmtree('runs')

    elif st.session_state.page == 1:
        with placeholder:
            sac.steps(
                items=[
                    sac.StepsItem(title='step 1', subtitle='Выбор продуктов', description='''Выберите продукты'''),
                    sac.StepsItem(title='step 2', subtitle='Подбор блюд',
                                  description='''ИИ подберёт для вас рецепты'''),
                    sac.StepsItem(title='step 3', subtitle='Корзина', description='''Корзина для заказа!'''),
                    sac.StepsItem(title='step 4', subtitle='Заказ', description='Заказ успешно совершён!'),
                ], format_func='title', placement='vertical', type='navigation', index=1
            )
            f = open('myfile.txt', 'r')
            food_list = f
            f.close()
            st.markdown(food_list)
            st.title("Выбор меню на неделю")
            if food_list:
                st.markdown(food_list)
                ask_gpt = st.button("Спросите рецепт блюда у ChatGPT")
                prompt = f'''Придумай блюдо, которое будет включать в себя хотя бы несколько продуктов, перечисленных пользователем. Ответь в формате Блюдо: *название*. Рецепт: список продуктов.'''
                completion = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "assistant", "content": prompt}
                    ]
                )
                response = completion.choices[0].message.content
                st.markdown(response)

                pattern = r'Блюдо:\s(.*)'

                # Use the re.search function to find the match
                match = re.search(pattern, response)

                # Check if a match was found
                if match:
                    # Extract the "название блюда" from the match
                    name = match.group(1)
                    dish_name = translator_1.translate(response)
                    image_bytes1 = query({
                        "inputs": dish_name,
                    })
                    image1 = Image.open(io.BytesIO(image_bytes1))
                    im1 = image1.save(f'geeks1.jpg')
                    path1 = f'geeks1.jpg'
                    st.image(path1, width=350)
                else:
                    st.error("Pattern not found in the input string.")
            else:
                st.error("Пустой список! Поднимитесь выше и добавьте в него блюда")


    elif st.session_state.page == 2:
        # Replace the chart with several elements:
        with placeholder.container():
            st.write("This is one element")
            st.write("This is another")
            st.metric("Page:", value=st.session_state.page)

    elif st.session_state.page == 3:
        placeholder.markdown(r"$f(x) = \exp{\left(x^🐈\right)}$")

    else:
        with placeholder:
            st.write("This is the end")
            st.button("Restart", on_click=restart)

if __name__ == "__main__":
    main()