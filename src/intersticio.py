from src.nivel import Nivel


class Intersticio:

    @staticmethod
    def _intersticio(numero_nivel: int) -> int:
        """Calcula número de meses de intersticio para alcançar determinado nível."""
        raise NotImplementedError("Método deve ser implementado em subclasses.")

    @classmethod
    def tempo_para_progredir(cls, nivel: Nivel, num_passos: int) -> int:
        """Calcula o tempo para progredir de um nível a qualquer outro, posterior.

        Implementado como classmethod para que subclasses possam sobrescrever
        o cálculo do interstício através de sua própria implementação de
        `_intersticio` e `cls._intersticio` seja chamado corretamente.
        """

        tempo = 0
        numero = nivel.numero
        for _ in range(num_passos):
            tempo += cls._intersticio(numero)
            numero += 1
        return tempo


class IntersticioE2(Intersticio):
    @staticmethod
    def _intersticio(numero_nivel: int) -> int:
        """Calcula número de meses de intersticio para alcançar determinado nível."""
        if numero_nivel <= 8:
            return 9
        if numero_nivel <= 28:
            return 12
        if numero_nivel <= 35:
            return 15
        return 24


class IntersticioE3(Intersticio):
    @staticmethod
    def _intersticio(numero_nivel: int) -> int:
        """Calcula número de meses de intersticio para alcançar determinado nível."""
        if numero_nivel <= 8:
            return 9
        if numero_nivel <= 28:
            return 12
        if numero_nivel <= 34:  # Diferença aqui em relação ao E2
            return 15
        return 24
