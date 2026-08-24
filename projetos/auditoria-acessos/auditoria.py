import pandas as pd
import matplotlib.pyplot as plt

# Carregamento das bases
df_logs = pd.read_csv('log_acessos_200_registros.csv')
df_rh = pd.read_csv('usuarios_ativos_200_registros.csv')

# Tarefa 1: Cruzamento de Dados (Contas Órfãs)
df_auditoria = pd.merge(df_logs, df_rh, on='usuario_id', how='left', indicator=True)
contas_orfas = df_auditoria[df_auditoria['_merge'] == 'left_only']

# Tarefa 2: Auditoria de Horário Comercial (08:00 - 18:00)
df_auditoria['data_hora'] = pd.to_datetime(df_auditoria['data_hora'])
fora_horario = df_auditoria[(df_auditoria['data_hora'].dt.hour < 8) |
(df_auditoria['data_hora'].dt.hour >= 18)]

# Tarefa 3: Identificação de IPs Externos
ips_externos = df_auditoria[(df_auditoria['status'] == 'Sucesso') &
(~df_auditoria['ip'].str.startswith('192.168'))]

# Tarefa 4: Visualização
categorias = ['Autorizados', 'Violação Horário', 'Contas Órfãs']
quantidades = [len(df_auditoria) - len(fora_horario) - len(contas_orfas),
len(fora_horario), len(contas_orfas)]

plt.bar(categorias, quantidades, color=['green', 'orange', 'red'])
plt.title('Riscos de Segurança')
plt.tight_layout()
plt.savefig('riscos_seguranca.png', dpi=150)
plt.show()

print(f'Contas órfãs: {len(contas_orfas)}')
print(f'Acessos fora do horário comercial: {len(fora_horario)}')
print(f'IPs externos com acesso bem-sucedido: {len(ips_externos)}')
print('Gráfico salvo em riscos_seguranca.png.')
