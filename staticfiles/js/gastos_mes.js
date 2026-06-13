export async function initGastosMes() {
    try {
        const response = await fetch('/charts/gastos_mes/');
        const datos = await response.json();

        let fecha = [];
        let monto = [];

        for(let i=0; i<datos.length;i++){
            fecha.push(datos[i].fecha);
            monto.push(datos[i].total);
        }

        const chart = echarts.init(document.getElementById("gastosDiaChart"));
        
        chart.setOption(
            {
                title: {
                },
                tooltip:{},
                toolbox: {
                    show : true,
                    feature : {
                        mark : {show: true},
                        dataView : {show: true, readOnly: false},
                        magicType: {show: true, type: ['line', 'bar']},
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                xAxis:{
                    data:fecha
                },
                yAxis:{
                    
                },
                series:{
                    name:"Total por día",
                    type:"line",
                    data:monto
                }
            }
        );
    }
    catch (error) {
    console.error("Se detectó un problema: ", error.message);
    }
}