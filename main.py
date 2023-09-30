import streamlit as st

def main():
    with st.sidebar:
        st.title("Умный холодильник")
        choice = st.radio("Навигация", ["Окно регистрации", "Холодильник", "Выбор меню на неделю", "Утверждение корзины", "Оповещение о заказе"])
    if choice == "Окно регистрации":
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
    elif choice == "Холодильник":
        st.subheader("Нажмите, чтобы посмотреть, какие продукты есть в холодильнике")
        b = st.button("Проверить")
        if b:
            st.image("friddge.jpg",width=550)
            st.text("В холодильнике есть:")
            st.text("Виноград (857 гр.)")
            st.text("Помидоры (344 гр.)")
            st.text("Черри (193 гр.)")
            st.error("У сыра истекает срок годности через 2 дня")
    elif choice == "Выбор меню на неделю":
        st.title("Выбор меню на неделю")
        col1, col2, col3, col4, col5, col6, col7 = st.columns([1, 1, 1, 1, 1, 1, 1])
        with col1:
            st.button('ПН')
        with col2:
            st.button('ВТ')
        with col3:
            st.button('СР')
        with col4:
            st.button('ЧТ')
        with col5:
            st.button('ПТ')
        with col6:
            st.button('СБ')
        with col7:
            st.button('ВС')
        st.subheader('Завтрак: яичница на помидорах')
        st.image('breakfast.jpg', width=550)
        st.success('Имеющиеся продукты: помидоры')
        st.error('Необходимо заказать: яйца')
        st.subheader('Обед: чечевичный крем-суп')
        st.image('lunch.jpg', width=550)
        st.error('Необходимо заказать: чечевица, лимон')
        st.subheader('Ужин: гречка по-купечески')
        st.image('dinner.jpg', width=550)
        st.success('Имеющиеся продукты: помидоры черри')
        st.error('Необходимо заказать: курица, гречневая крупа, морковь')
    elif choice == "Утверждение корзины":
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
    elif choice == "Оповещение о заказе":
        st.title("Вы успешно совершили заказ!")
        st.divider()
        st.subheader("Ваш курьер уже в пути!")
        st.subheader("Приблизительное время доставки:")
        st.subheader("15:44")
        st.balloons()


if __name__ == "__main__":
    main()