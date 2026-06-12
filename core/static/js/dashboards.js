import { cargarKPIs } from './kpi.js';
import { initGastosMes } from './gastos_mes.js';
import { initGastosEstatus } from './gastos_estatus.js';
import { initPagosBanco } from './bancosGrafico.js';
import { initGastosCliente } from './gastos_cliente.js';

window.addEventListener(
    'load',
    async function(){
        const resultados = await Promise.allSettled([
            cargarKPIs(),
            initGastosMes(),
            initGastosEstatus(),
            initPagosBanco(),
            initGastosCliente()
        ]);

        console.log(resultados);

    }
);