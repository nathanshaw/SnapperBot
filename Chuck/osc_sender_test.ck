// launch with OSC_recv.ck

// host name and port
//"10.0.1.5" => string hostname;
"localhost" => string hostname;
40000 => int port;

// get command line
if( me.args() ) me.arg(0) => hostname;
if( me.args() > 1 ) me.arg(1) => Std.atoi => port;

// send object
OscOut xmit;

// aim the transmitter
xmit.dest( "10.0.1.5" , port );

// infinite time loop
while( true )
{
    // start the message...
    xmit.start( "/switch" );
    <<<"----------------">>>;
    // add float arg
    //Math.random2( 0, 5 ) => int temp => xmit.add;
    0 => int temp => xmit.add;
    
    <<< temp >>>;
    Math.random2( 0, 2 ) => temp => xmit.add;
    <<< temp >>>;
    Math.random2( 1, 8 ) => temp => xmit.add;
    <<< temp >>>;
    // send
    xmit.send();
    <<<"----------------">>>;
    // advance time
    0.5::second => now;
}
