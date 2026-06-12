from .models import *

pagos = Pagos.objects.filter(gasto_id = 1,estatus="APPROVED")
print(pagos)