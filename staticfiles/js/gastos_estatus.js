export async function initGastosEstatus() {
    try {
        const response = await fetch('/charts/gastos_estatus/');
        const datos = await response.json();

        let datos_grafico = [];

        for(let i=0; i<datos.length;i++){
            datos_grafico.push(
                {
                    name: datos[i].estatus,
                    value: datos[i].monto
                }
            );
        }

        const chart = echarts.init(document.getElementById("gastosEstatusChart"));
        
        chart.setOption(
            {
                title: {
                
                },
                legend:{
                    bottom:'0%'
                },
                tooltip:{
                },
                toolbox: {
                    show : true,
                    feature : {
                        mark : {show: true},
                        dataView : {show: true, readOnly: false},
                        restore : {show: true},
                        saveAsImage : {show: true}
                    }
                },
                series:{
                    name:"Gastos",
                    type:"pie",
                    radius:[
                        "40%",
                        "70%"
                    ],
                    data: datos_grafico
                }
            }
        );
    }
    catch (error) {
    console.error("Se detectó un problema: ", error.message);
    }
}