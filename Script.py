import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from quantumnet.components import Network, Host
from quantumnet.objects import Qubit, Logger
import json
import random

# Captura o número de rounds a partir dos argumentos (opcional)
rounds = int(sys.argv[1]) if len(sys.argv) > 1 else 1

# Ativa o Logger
Logger.activate(Logger)

# Inicializa uma nova rede
Logger.get_instance().log(f"Simulação inicializando...")
rede = Network()
rede.set_ready_topology("Grade", 3, 4)
rede.draw()

#define a fidelidade inicial
fidelidade_inicial = 0.9

# Patching do método create_epr_pair
original_create_epr_pair = rede._physical.create_epr_pair  # Salva a função original


def patched_create_epr_pair(fidelity=None, increment_timeslot=False, increment_eprs=False):
    """Sobrescreve a fidelidade padrão com a definida no script."""
    fidelity = fidelity if fidelity is not None else fidelidade_inicial
    return original_create_epr_pair(fidelity, increment_timeslot, increment_eprs)


# Substitui o método da camada física pelo patch
rede._physical.create_epr_pair = patched_create_epr_pair


# Define os hosts
alice = rede.get_host(1)
bob = rede.get_host(2)

# Obtém a fidelidade inicial dos pares EPR entre Alice e Bob
initial_epr_pairs = rede.get_eprs_from_edge(alice.host_id, bob.host_id)
initial_fidelity = None
if not initial_epr_pairs:
                # Cria um novo par EPR com fidelidade inicial (pode ser ajustado conforme necessário)
                new_epr = rede._physical.create_epr_pair(  increment_timeslot=False)
                rede._physical.add_epr_to_channel(new_epr, (alice, bob))
                
                # Medir a fidelidade do novo par EPR
                initial_fidelity = new_epr.get_current_fidelity()
                
                # Remove o par EPR após a medição
                rede._physical.remove_epr_from_channel(new_epr, (alice, alice))


if initial_epr_pairs:
    initial_fidelity = initial_epr_pairs[-1].get_current_fidelity()

# Informações do canal
channel_info = rede.get_channel_info(alice.host_id, bob.host_id)
canal_tipo = channel_info.get('type', 'desconhecido')



#pode selecionar o tipo de canal, por exemplo: XZ, Y, Z
# if canal_tipo not in ['XZ']:
#     Logger.get_instance().log(f"Canal do tipo '{canal_tipo}' ignorado. Simulação não será executada para este canal.")
#     result = {
#         "simulation": rounds,
#         "status": "ignored",
#         "reason": f"Canal do tipo '{canal_tipo}' não avaliado."
#     }
#     print(json.dumps(result, indent=4))
#     sys.exit(1)  # Continua a execução das próximas simulações sem interrupção

# Gera uma request de fidelidade alvo aleatória
request = 0.95  #random.uniform(0.75, 0.96)


#ignora requests que não podem ser atingidas
# if request > 1.4 * initial_fidelity:
    
#     result = {
#         "simulation": rounds,
#         "success": False,
#         "reason": "Request impossivel de atingir",
#         "initial_fidelity": initial_fidelity,
#         "final_fidelity": initial_fidelity
#     }
#     print(json.dumps(result, indent=4))
#     sys.exit(0)  # Interrompe o script para pular a simulação


#define o tipo de purificação, sendo pumping, symmetric, symmetric_proposal, pumping_proposal
tipo_de_purificacao = "pumping_proposal"

# Define o tipo de estimativa com base no tipo de purificação
if tipo_de_purificacao == "pumping":
    tipo_de_estimativa = "pumping"
elif tipo_de_purificacao == "symmetric":
    tipo_de_estimativa = "symmetric"
elif tipo_de_purificacao == "symmetric_proposal":
    tipo_de_estimativa = "symmetric"  # "symmetric_proposal" usa "symmetric" para a estimativa
elif tipo_de_purificacao == "pumping_proposal":
    tipo_de_estimativa = "pumping"  # "pumping_proposal" usa "pumping" para a estimativa
else:
    raise ValueError(f"Tipo de purificação inválido: {tipo_de_purificacao}")


# Estima o número de rounds necessários para atingir a fidelidade alvo
rounds_estimation = rede.linklayer.round_estimates(alice.host_id, bob.host_id, request, tipo_de_estimativa)
required_rounds = rounds_estimation.get(tipo_de_estimativa, {}).get("rounds", rounds)

Logger.get_instance().log(f"Fidelidade inicial: {initial_fidelity}")
Logger.get_instance().log(f"Request de fidelidade alvo: {request}")
Logger.get_instance().log(f"Tipo de canal: {canal_tipo}")
Logger.get_instance().log(f"Estimativa de rounds necessários: {required_rounds}")

# Executa o agendamento de purificação com os rounds estimados
success = rede.linklayer.purification_scheduling(alice.host_id, bob.host_id,tipo_de_purificacao, required_rounds)

# Obtém a fidelidade final após o agendamento
final_epr_pairs = rede.get_eprs_from_edge(alice.host_id, bob.host_id)
final_fidelity = None
if final_epr_pairs:
    final_fidelity = final_epr_pairs[-1].get_current_fidelity()
else:
    # Se não houver pares EPRs no final, define a fidelidade final como a inicial
    final_fidelity = initial_fidelity

if final_fidelity is not None and final_fidelity >= request:
    success = True
    Logger.get_instance().log(f"Purificação bem-sucedida: Fidelidade final ({final_fidelity}) >= Request ({request}).")
else:
    success = False
    Logger.get_instance().log(f"Purificação falhou: Fidelidade final ({final_fidelity}) < Request ({request}).")

# Loga o sucesso ou falha da purificação e fidelidade final
Logger.get_instance().log(f"Sucesso da purificação: {success}")
Logger.get_instance().log(f"Fidelidade final: {final_fidelity}")

# Armazena o resultado da simulação em JSON
result = {
    "simulation": rounds,
    "success": success,
    "estimated_rounds": required_rounds,
    "request": request,
    "channel_info": canal_tipo,
    "initial_fidelity": initial_fidelity,
    "final_fidelity": final_fidelity
}

# Chama a função linklayermetrics incluindo a métrica de erro
rede.linklayermetrics(
        simulation_number=rounds,
        success=success,
        metrics_requested=[
            "Timeslot Total",
            "EPRs Criados",
            "Pares Eprs Consumidos",
            "Fidelidade Média dos Eprs",
            "Erro"  # Renomeado para capturar qualquer tipo de erro
        ],
        output_type="csv",  # Exporta para CSV
        file_name="link_metrics_output.csv"
    )


# Apenas imprime o JSON do resultado, sem outras saídas
print(json.dumps(result, indent=4))
