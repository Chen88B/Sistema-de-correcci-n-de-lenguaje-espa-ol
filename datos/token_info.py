class TokenInfo:
    def __init__(self, texto,base,categoria,depedencia,cabeza,cabeza_indice,morfologicos,etiqueta,posicion,idx_inicio, idx_final,forma,es_stop,es_numero,es_email,es_url):
        self._texto = texto # Forma exacta del token
        self._base = base # Lemma, es decir, la forma basica de un palabra, infinitivo
        self._categoria = categoria #Categoria gramatica, NOUN=Sustantivos, VERB=verbo, ADJ=Adjectivo y etc
        self._depedencia = depedencia # Relacion sintacticas
        self._cabeza = cabeza #Palabra que depende este palabra
        self._cabeza_indice = cabeza_indice #Indice de la cabeza
        self._morfologicos = morfologicos #Diccionario que nos dice la tiempo, genero, numero, modo y etc
        self._etiqueta = etiqueta #Categoria especifica, tiempo verbal, genero, caso y etc
        self._posicion = posicion #Indice de token
        self._idx_inicio = idx_inicio # Indice del caracter inicial (ej: 0)
        self._idx_final = idx_final # Indice del caracter final (ej: 5)
        self._forma = forma #Patrones de forma de un token
        self._es_stop = es_stop #Si es palabra vacia como de, la, que, para y etc
        self._es_numero = es_numero #Si es un numero
        self._es_email = es_email #Si es un email
        self._es_url = es_url #Si es un url

    """   
   Metodo para regresa la TokenInfor en un forma mas sencilla de entender
   Parametros:Ninguno
   Devuelve:String
   """
    def representar(self):
        return (
            f"TokenInfo(texto='{self._texto}', base='{self._base}', cat='{self._categoria}', "
            f"dep='{self._depedencia}', cabeza='{self._cabeza}', pos={self._posicion})"
            f"indices=[{self._idx_inicio}:{self._idx_final}])"
        )

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

    @property
    def etiqueta(self):
        return self._etiqueta

    @property
    def posicion(self):
        return self._posicion

    @property
    def forma(self):
        return self._forma

    @property
    def es_stop(self):
        return self._es_stop

    @property
    def es_numero(self):
        return self._es_numero

    @property
    def es_email(self):
        return self._es_email

    @property
    def es_url(self):
        return self._es_url

    @property
    def cabeza_indice(self):
        return self._cabeza_indice

    @property
    def idx_inicio(self):
        return self._idx_inicio

    @property
    def idx_final(self):
        return self._idx_final
