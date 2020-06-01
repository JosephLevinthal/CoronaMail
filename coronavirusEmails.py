from selenium import webdriver


class CoronaVirus:
    import schedule
    import time

    # Função que inicia o contato com o Google Chrome para o web scraping
    def __init__(self):
        self.driver = webdriver.Chrome("chromedriver.exe")

    # Função que faz o web scraping dos dados da CNN, NBC, CNBC e organiza em um dataframe
    def manchetes(self):
        print("oi")
        from datetime import date

        today = date.today()

        d = today.strftime("%m-%d-%y")
        print("date=", d)

        cnn_url = "https://edition.cnn.com/world/live-news/coronavirus-pandemic-{}-intl/index.html".format(
            d
        )

        from bs4 import BeautifulSoup
        import requests

        html = requests.get(cnn_url).text
        soup = BeautifulSoup(html)

        nbc_url = "https://www.nbcnews.com/health/coronavirus"
        cnbc_rss_url = "https://www.cnbc.com/id/10000108/device/rss/rss/html"

        urls = [cnn_url, nbc_url, cnbc_rss_url]
        formats = ["html.parser", "html.parser", "xml"]
        tags = ["h2", "h2", "title"]
        website = ["CNN", "NBC", "CNBC"]

        crawl_len = 0
        for url in urls:
            print("Crawling web page.........{}".format(url))
            response = requests.get(url)
            soup = BeautifulSoup(response.content, formats[crawl_len])

            # for link in soup.find_all(tags[crawl_len]):
            # if len(link.text.split(" ")) > 4:
            # print("Headline : {}".format(link.text))
            # crawl_len = crawl_len + 1

        crawl_len = 0
        news_dict = []
        for url in urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, formats[crawl_len])

            for link in soup.find_all(tags[crawl_len]):
                if len(link.text.split(" ")) > 4:

                    news_dict.append(
                        {
                            "website": website[crawl_len],
                            "url": url,
                            "headline": link.text,
                        }
                    )
            crawl_len = crawl_len + 1

        import pandas as pd

        news_df = pd.DataFrame(news_dict)
        pd.set_option("max_colwidth", 800)
        print(news_df.count())

        news_df["website"] = news_df["website"].astype(str)
        news_df["url"] = news_df["url"].astype(str)
        news_df["headline"] = news_df["headline"].astype(str)
        print(news_df.website.unique())
        print(news_df.dtypes)

        noticia_CNN = news_df["url"][1]
        noticia_NBC = "https://www.nbcnews.com/health/coronavirus"
        noticia_CNBC = "https://www.cnbc.com/coronavirus/"

        df_headlines = news_df.groupby("website").head(4).reset_index(drop=True)

        global manchetesPrint
        manchetesPrint = str(
            "Principais manchetes do dia: \n\n"
            + "CNN - "
            + noticia_CNN
            + "\n"
            + "1- "
            + df_headlines["headline"][1]
            + "\n"
            + "2- "
            + df_headlines["headline"][2]
            + "\n"
            + "3- "
            + df_headlines["headline"][3]
            + "\n\n"
            + "NBC - "
            + noticia_NBC
            + "\n"
            + "1- "
            + df_headlines["headline"][4]
            + "\n"
            + "2- "
            + df_headlines["headline"][6]
            + "\n"
            + "3- "
            + df_headlines["headline"][7]
            + "\n\n"
            + "CNBC - "
            + noticia_CNBC
            + "\n"
            + "1- "
            + df_headlines["headline"][8]
            + "\n"
            + "2- "
            + df_headlines["headline"][9]
            + "\n"
            + "3- "
            + df_headlines["headline"][10]
        )

    # Função que faz o web scraping dos dados sobre atualizações do coronavirus e envia um e-mail para a lista de e-mails
    def get_data(self):
        country = "Brazil"
        try:
            country_contains = "contains(., '%s')" % country

            self.driver.get("https://www.worldometers.info/coronavirus/")
            table = self.driver.find_element_by_xpath(
                '//*[@id="main_table_countries_today"]/tbody[1]'
            )

            country_element = table.find_element_by_xpath("//td[%s]" % country_contains)
            row = country_element.find_element_by_xpath("./..")
            total_cases = row.find_element_by_xpath("//tr[%s]/td[3]" % country_contains)
            new_cases = row.find_element_by_xpath("//tr[%s]/td[4]" % country_contains)
            total_deaths = row.find_element_by_xpath(
                "//tr[%s]/td[5  ]" % country_contains
            )
            new_deaths = row.find_element_by_xpath("//tr[%s]/td[6]" % country_contains)
            active_cases = row.find_element_by_xpath(
                "//tr[%s]/td[8]" % country_contains
            )
            total_recovered = row.find_element_by_xpath(
                "//tr[%s]/td[7]" % country_contains
            )
            serious_critical = row.find_element_by_xpath(
                "//tr[%s]/td[9]" % country_contains
            )
            tot_1m = row.find_element_by_xpath("//tr[%s]/td[9]" % country_contains)

            print("Country: " + str(country_element.text))
            print("Total cases: " + str(total_cases.text))
            print("New cases: " + str(new_cases.text))
            print("Total deaths: " + str(total_deaths.text))
            print("New deaths: " + str(new_deaths.text))
            print("Active cases: " + str(active_cases.text))
            print("Total recovered: " + str(total_recovered.text))
            print("Serious, critical cases: " + str(serious_critical.text))
            print("Total cases/1M population: " + str(tot_1m.text))

            import smtplib
            import email.utils
            import datetime
            import schedule
            from email.mime.multipart import MIMEMultipart
            from email.mime.text import MIMEText
            from email.mime.image import MIMEImage

            dt = datetime.datetime.today()

            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login("insert your email here", "insert your app password here")

            subject = (
                "Estatisticas do COVID-19 em: "
                + "Brasil"  # str(country_element.text)
                + ", no dia "
                + dt.strftime("%d-%m-%Y")
            )
            body = (
                (
                    "--------------------------------\n"
                    + "Dados de: "
                    + "Brasil"  # str(country_element.text)
                    + "\
            \n\nAtualizacao dos casos de COVID-19:\
            \n\nNumero total: "
                    + str(total_cases.text)
                    + "\
            \nCasos ativos: "
                    + str(active_cases.text)
                    + "\
            \nCasos criticos: "
                    + str(serious_critical.text)
                    + "\
            \n\nTotal de mortes: "
                    + str(total_deaths.text)
                    + "\
            \nTotal de recuperados: "
                    + str(total_recovered.text)
                    + "\
             \n\nNovos casos (em relacao ao dia anterior): "
                    + str(new_cases.text)
                    + "\
            \nNovas mortes (em relacao ao dia anterior): "
                    + str(new_deaths.text)
                    + "\n--------------------------------\
            \n\nOs dados foram obtidos de https://www.worldometers.info/coronavirus/ e sao atualizados em: 00:00(GMT+0)."
                    + "\nNao deixe de seguir as recomendacoes medicas!"
                    + "\n\n--------------------------------\n"
                    + manchetesPrint
                    + "\n\n\nEste e-mail foi enviado automaticamente. Caso nao queira mais receber, mande uma mensagem :D"
                    + "\nhttps://www.facebook.com/joseph.viana"
                    + "\nhttps://www.linkedin.com/in/josephlevinthal/"
                    + "\n\n"
                )
                .encode("ascii", "ignore")
                .decode("ascii")
            )
            listaEmails = [
                "insertemailshere"
            ]

            msg = f"Subject: {subject}\n\n{body}"
            server.sendmail("Coronavirus", listaEmails, msg)
            print("SENT!")
            server.quit()

            self.driver.close()
        except Exception as e:
            print(e)
            self.driver.quit()


if __name__ == "__main__":

    bot = CoronaVirus()
    bot.manchetes()
    bot.get_data()
