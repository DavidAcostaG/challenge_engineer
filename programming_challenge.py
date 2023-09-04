import pandas as pd
import requests
import json

#########################################################    PREGUNTA 1    #########################################################
#Se usan funciones lambda por simplicidad, ya que solo se usaràn una vez en el còdigo
#Funcion para obtener la respuesta del API de Stack
url_reader = lambda url: requests.get(url) if requests.get(url).status_code == 200 else print(f'Error with the request: Code {requests.get(url).status_code}')

url_challenge = "https://api.stackexchange.com/2.2/search?order=desc&sort=activity&intitle=perl&site=stackoverflow"

url_response = url_reader(url_challenge)

#Funciòn para convertir a JSON la data de la respuesta del request
response_to_json = lambda response: json.loads(response.text) if isinstance(json.loads(response.text), dict) else print('Response body does not contain a valid json format')

json_data = response_to_json(url_response)

#La informaciòn de interés está en la llave ITEMS, convertimos el contenido de esta llave en un dataframe de pandas
df_stack = pd.json_normalize(json_data['items'])

df_stack.columns

#########################################################    PREGUNTA 2 #########################################################
#Para StackOverflow una respuesta contestada se considera còmo tal, si al menos tiene una respuesta votada, considerando este caso:
print("PREGUNTA 2\n")
print(f'Respuestas contestadas según StackOverflow:\n')
print(df_stack['is_answered'].value_counts().values[0])
print(f'Respuestas no contestadas según StackOverflow:\n')
print(df_stack['is_answered'].value_counts().values[1])

#Si consideramos cualquier respuesta, sin importar las votaciones entonces el resultado serìa:
print(f'Respuestas contestadas:\n')
print(sum(df_stack['answer_count']> 0))
print(f'Respuestas no contestadas:\n')
print(sum(df_stack['answer_count']== 0))

#########################################################    PREGUNTA 3    #########################################################
#Dado que la data està a nivel pregunta, no tenemos las vistas a nivel respuesta, pero si las vistas de una pregunta, en ese caso, la pregunta con menor vistas es la siguiente:
#Es una pregunta sin respuesta dada la definiciòn de stack pàra respuestas aceptadas
min_view_count = df_stack['view_count'].min()
print("PREGUNTA 3\n")
print('Pregunta con menos vistas \n question_id:',df_stack[df_stack['view_count'] == min_view_count]['question_id'].values)

#########################################################    PREGUNTA 4    #########################################################
dates_cols = ['last_activity_date',
                  'creation_date',
                  'last_edit_date',
                  'closed_date']
for date_col in dates_cols:
    df_stack[date_col] = pd.to_datetime(df_stack[date_col], unit='s')

#Nuevamente con esta informaciòn no es posible saber la fecha a nivel respuesta, ùnicamente a nivel pregunta, en este caso el resultado serìa el siguiente:
min_date = df_stack['creation_date'].min()
max_date = df_stack['creation_date'].max()
print("PREGUNTA 4")
print('Pregunta màs antigua \n question_id:', df_stack[df_stack['creation_date'] == min_date]['question_id'].values)
print('Pregunta màs reciente \n question_id:', df_stack[df_stack['creation_date'] == max_date]['question_id'].values)

#########################################################    PREGUNTA 5    #########################################################
#Ocurre lo mismo que en anteriores puntos, pero podemos obtener la pregunta del owner con mejor reputaciòn:
best_owner = df_stack['owner.reputation'].max()
print("PREGUNTA 5\n")
print('Pregunta del mejor owner \n question_id:', df_stack[df_stack['owner.reputation'] == best_owner]['question_id'].values)