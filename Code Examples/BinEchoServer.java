import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.ServerSocket;
import java.net.Socket;


public class BinEchoServer {

	public static void main(String[] args) {
		if ( args.length != 1 )
		{
			System.out.println( "Usage:" );
			System.out.println( "   java BinEchoServer <port number>" );
			return;
		}
		
		int port= Integer.valueOf( args[0] );		
		try
		{
			ServerSocket server_socket= new ServerSocket( port );
			Socket remote_socket= server_socket.accept();
			DataOutputStream output= new DataOutputStream( remote_socket.getOutputStream() );
			DataInputStream input= new DataInputStream( remote_socket.getInputStream() );				

			int recv_int_val= input.readInt();
			String message= input.readUTF();
			System.out.println( "Received from client: " + recv_int_val );			
			System.out.println( "Received from client: " + message );
			output.writeInt( recv_int_val );
			output.writeUTF( message );
			remote_socket.close();
			server_socket.close();
		}
		catch ( Exception e )
		{
			System.out.println( e.getMessage() );
		}
	}

}
