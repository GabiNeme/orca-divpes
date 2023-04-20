from src.cargo import Nivel


class Intersticio:
    @staticmethod
    def _intersticio(numero_nivel: int) -> int:
        """Calcula número de meses de intersticio para alcançar determinado nível."""
        if numero_nivel <= 8:
            return 9
        if numero_nivel <= 28:
            return 12
        if numero_nivel <= 47:
            return 15
        return 24

    @staticmethod
    def tempo_para_progredir(nivel: Nivel, num_passos: int) -> int:
        """Calcula o tempo para progredir de um nível a qualquer outro, posterior."""

        tempo = 0
        numero = nivel.numero
        for _ in range(num_passos):
            tempo += Intersticio._intersticio(numero)
            numero += 1
        return tempo
