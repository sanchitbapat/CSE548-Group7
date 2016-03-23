import org.apache.spark._
import org.apache.spark.graphx.
// To make some of the examples work we will also need RDD
import org.apache.spark.rdd.RDD
import org.apache.spark.SparkConf
import org.apache.spark.SparkContext

class Scalateststep{
	def main(args: Array[String]) {
		val conf=new SparkConf().setAppName("test")
		//val sc: SparkContext
//		val sc = new SparkContext("spark://spark://192.168.0.13:7077", "Scala GraphX",System.getenv("SPARK_HOME"), SparkContext.jarOfClass(this.getClass))
		val sc=new SparkContext(conf)

		//val users:RDD[(VertexId, (String))] = sc.textFile("users.txt").map { line =>line.split(",").map(VertexId(fields(0).toLong), String(fields(1)))}




		val vertxText = sc.textFile("hdfs://master:54310/user/hadoop/vertexData.csv")
		val edgesText = sc.textFile("hdfs://master:54310/user/hadoop/edgeData.csv")

		def pipeSplit(line: String) : Array[String] = { line.split(',') }
		def pageHash(nodeId: String): VertexId = {
		  nodeId.hashCode.toLong
		}
		def nonNull(s: String): Double = {
		  if (s == "") Double.NaN else s.toDouble
		}

		val verticesArray = vertxText.map(pipeSplit)
		val edgesArray = edgesText.map(pipeSplit)

		/*case class VertxAttributes(
			nodeId: Long
			, color: String
		) extends Serializable

		val verticesAttr = verticesArray.map{ data =>
		  	val nodeId = data(0).toLong
			val color = data(1)
		}*/

		val vertices: RDD[(VertexId, (String))] = verticesArray.map{ attributes =>
			val nodeId = attributes(0).toLong
			val color = attributes(1)
			(nodeId,color)
		}



		val edges: RDD[Edge[String]] = edgesArray.map { data =>
		  val srcVid = data(0).toLong
		  val dstVid = data(1).toLong
		  val relationship = data(2)
		  Edge(srcVid, dstVid, relationship)
		}

		val graph = Graph(vertices, edges)




		//val users = sc.textFile("users.txt").map { line =>line.split(",").flatMap(array => array).map(x=>(x.toLong, x))}

		//val users = sc.textFile("relations.txt").map { line =>line.split(",").map(line => Edge(line(0).toLong, line(1).toLong, "color"))}

		/*val users: RDD[(VertexId, (String))] =
		  sc.parallelize(Array((3L, ("green")), (7L, ("blue")),
				       (5L, ("blue")), (2L, ("green")),
				       (4L, ("red"))))*/
		// Create an RDD for edges
		/*val relationships: RDD[Edge[String]] =
		  sc.parallelize(Array(Edge(3, 7L, "color"),    Edge(5L, 3L, "color"),
				       Edge(2L, 5L, "color"), Edge(5L, 7L, "color"),
				       Edge(4L, 0L, "color"),   Edge(5L, 0L, "color")))*/
		// Define a default user in case there are relationship with missing user
		val defaultUser = ("Missing")
		// Build the initial Graph
		//val graph = Graph(edges, vertices)
		// Notice that there is a user 0 (for which we have no information) connected to users
		// 4 (peter) and 5 (franklin).
		graph.triplets.map(
		    triplet => triplet.srcAttr + " is the " + triplet.attr + " of " + triplet.dstAttr
		  ).collect.foreach(println(_))
		// Remove missing vertices as well as the edges to connected to them
		val blueGraph = graph.subgraph(vpred = (id, attr) => attr != "Missing"&&attr != "green"&&attr != "red")
		val greenGraph = graph.subgraph(vpred = (id, attr) => attr != "Missing"&&attr != "blue"&&attr != "red")
		val redGraph = graph.subgraph(vpred = (id, attr) => attr != "Missing"&&attr != "blue"&&attr != "green")
		// The valid subgraph will disconnect users 4 and 5 by removing user 0
		//blueGraph.vertices.collect.foreach(println(_))
		/*validGraph.triplets.map(
		    triplet => triplet.srcId + " is the " + triplet.attr + " of " + triplet.dstId
		  ).repartition(1).saveAsTextFile("/home/hduser1/temptext.txt")*/
		/*blueGraph.triplets.map(
		    triplet => triplet.srcId + " is the " + triplet.attr + " of " + triplet.dstId
		  ).collect.foreach(println(_))*/
		//greenGraph.triplets.collect.foreach(println(_))
		greenGraph.edges.map(edge=>edge.srcId+","+edge.dstId).repartition(1).saveAsTextFile("hdfs://master:54310/user/hadoop/green")
		redGraph.edges.map(edge=>edge.srcId+","+edge.dstId).repartition(1).saveAsTextFile("hdfs://master:54310/user/hadoop/red")
		blueGraph.edges.map(edge=>edge.srcId+","+edge.dstId).repartition(1).saveAsTextFile("hdfs://master:54310/user/hadoop/blue")
		greenGraph.triplets.collect.foreach(println(_))
		//edges.collect.foreach(println(_))
	}
}
