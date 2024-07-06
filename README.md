# serial-oscilosc-pio
serial osciloscópio
com py qt > https://www.qt.io/
um sistema completo para um osciloscópio de 2 canais que puxa os dados da serial
baixe Divirta-se faça suas modificações se fizer alguma modificação por favor poste nos > https://github.com/Valdemir-DSW/serial-oscilosc-pio/issues
a única função que não foi completamente implementada e não está funcionando corretamente é dar leitura de frequência <<<<
para enviar os dados e muito simples eu deixei um exemplo de arduíno mas vou explicar melhor após estabelecer a conexão

![image](https://github.com/Valdemir-DSW/serial-oscilosc-pio/assets/134114016/6f56f38f-57c9-4999-a21e-ae1923b8218a)

enviar os 2 sinais separados por virgula ele aceita valores de zero até 1023 sendo o valor 512 como um valor central 
quando estiver na função de entrada de sinal 1x se o valor da serial for zero ele vai definir o visor do voltímetro como −100 e se for 1023 como 100+ se for 512 ele vai deixar o voltímetro zerado simplesmente assim
versão em executável caso queira > https://drive.google.com/file/d/1NEJ1tIfk6tG78rcH2U5WGQs4ps4fa3D5/view?usp=sharing

claro que a programação do Arduino não está pronta você deve fazer a lógica para medir o que você quiser da forma correta
pode usar qualquer placa com comunicação serial
![image](https://github.com/Valdemir-DSW/serial-oscilosc-pio/assets/134114016/7c742875-a99c-40f6-b947-4162b5d471e3)
