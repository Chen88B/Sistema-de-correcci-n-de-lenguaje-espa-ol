class TokenInfo:
    def __init__(self, texto,base,categoria,depedencia,cabeza,morfologicos):
        self._texto = texto
        self._base = base
        self._categoria = categoria
        self._depedencia = depedencia
        self._cabeza = cabeza
        self._morfologicos = morfologicos

    """   
   Metodo para regresa la TokenInfor en un forma mas sencilla de entender
   Parametros:Ninguno
   Devuelve:String
   """
    def representar(self):
        return f"TokenInfo(texto={self._texto}, categoria={self._categoria}, cabeza={self._cabeza})"

    """Desde aqui, todos son metodos get y set de los atributos"""
    @property
    def texto(self):
        return self._texto

    @property
    def base(self):
        return self._base

    @property
    def categoria(self):
        return self._categoria

    @property
    def depedencia(self):
        return self._depedencia

    @property
    def cabeza(self):
        return self._cabeza

    @property
    def morfologicos(self):
        return self._morfologicos

    @texto.setter
    def texto(self,texto):
        self._texto = texto

    @base.setter
    def base(self,base):
        self._base = base

    @categoria.setter
    def categoria(self,categoria):
        self._categoria = categoria

    @depedencia.setter
    def depedencia(self,depedencia):
        self._depedencia = depedencia

    @cabeza.setter
    def cabeza(self,cabeza):
        self._cabeza = cabeza

    @morfologicos.setter
    def morfologicos(self,morfologicos):
        self._morfologicos = morfologicos