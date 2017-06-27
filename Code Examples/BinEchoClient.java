import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.InetAddress;
import java.net.Socket;
import java.io.DataOutputStream;
import java.io.DataInputStream;

public class BinEchoClient {

	public static void main(String[] args) {
		if ( args.length != 1 )
		{
			System.out.println( "Usage:" );
			System.out.println( "   java BinEchoClient <port number>" );
			return;
		}
		
		int port= Integer.valueOf( args[0] );		
		try
		{
			// input the message from standard input
			BufferedReader reader= new BufferedReader( 
					 new InputStreamReader(System.in) );
			
			System.out.print( "Enter an integer: " );
			String int_str= reader.readLine();
			int int_val= Integer.valueOf( int_str ).intValue();
			System.out.print( "Enter a message: " );
			String message= reader.readLine();
			
			InetAddress loopback= InetAddress.getLoopbackAddress();
			Socket client_socket= new Socket( loopback, port );
			DataOutputStream output= new DataOutputStream( client_socket.getOutputStream() );
			DataInputStream input= new DataInputStream( client_socket.getInputStream() );				

			output.writeInt( int_val );
			output.writeUTF( message );
			int recv_int_val= input.readInt();
			message= input.readUTF();
			System.out.println( "Received integer: " + recv_int_val );
			System.out.println( "Received message: " + message );
			client_socket.close();
		}
		catch ( Exception e )
		{
			System.out.println( e.getMessage() );
		}
	}

}
