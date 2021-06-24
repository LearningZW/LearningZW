package datastruct;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.PrintWriter;
import java.io.Reader;
import java.io.StringWriter;
import java.util.LinkedList;
import java.util.List;
import java.util.Scanner;

public class CutVerEdge {

/*用于标记已访问过的顶点*/
private boolean[] marked;

/*三个数组的作用不再解释*/
private int[] low;
private int[] dfn;
private int[] parent;

/*用于标记是否是割点*/
private boolean[] isCutVer;

/*存储割点集的容器*/
private List<Integer> listV;

/*存储割边的容器，容器中存储的是数组，每个数组只有两个元素，表示这个边依附的两个顶点*/
private List<int[]> listE;

private UndirectedGraph ug;
private int visitOrder;/*时间戳变量*/

/*定义图的边*/
public static class Edge{

/*边起始顶点*/
private final int from;

/*边终结顶点*/
private final int to;

public Edge(int from, int to){
this.from = from;
this.to= to;
}

public int from(){
return this.from;
}

public int to(){
return this.to;
}

public String toString(){
return "[" + from + ", " + to +"] ";
}
}

/*定义无向图*/
  public static class UndirectedGraph{

private int vtxNum;/*顶点数量*/
private int edgeNum;/*边数量*/

/*临接表*/
private LinkedList<Edge>[] adj;

/*无向图的构造函数,通过txt文件构造图，无权值*/
@SuppressWarnings("unchecked")
public UndirectedGraph(Reader r){

BufferedReader br = new BufferedReader(r);
Scanner scn = new Scanner(br);

/*图中顶点数*/
vtxNum = scn.nextInt();
/*图中边数*/
edgeNum = scn.nextInt();

adj = (LinkedList<Edge>[])new LinkedList[vtxNum];

for(int i = 0; i < vtxNum; i++){
adj[i] = new LinkedList<Edge>();
}

/*无向图,同一条边，添加两次*/
for(int i = 0; i < edgeNum; i++){
int from = scn.nextInt();
int to = scn.nextInt();
Edge e1 = new Edge(from, to);
Edge e2 = new Edge(to, from);
adj[from].add(e1);
adj[to].add(e2);
}
scn.close();
}

/*图的显示方法*/
@Override
public String toString(){
StringWriter sw = new StringWriter();
PrintWriter pw = new PrintWriter(sw);
for (int i = 0; i < vtxNum; i++) {
pw.printf(" %-3d:  ", i);
for (Edge e : adj[i]) {
    pw.print(e);
}
pw.println();
}
return sw.getBuffer().toString();
}

/*返回顶点个数*/
  public int vtxNum(){
return vtxNum;
}

/*返回边的数量*/
  public int edgeNum(){
return edgeNum;
}

}

public CutVerEdge(UndirectedGraph ug){

    this.ug = ug;

marked = new boolean[ug.vtxNum()];

low = new int[ug.vtxNum()];
dfn = new int[ug.vtxNum()];
parent = new int[ug.vtxNum()];

isCutVer = new boolean[ug.vtxNum()];

listV = new LinkedList<Integer>();
listE = new LinkedList<int[]>();

/*调用深度优先遍历，求解各个顶点的dfn值和low值*/
           dfs();
}


private void dfs(){

    int childTree  = 0;
marked[0] = true;
visitOrder = 1;
parent[0] = -1;

for(Edge e : ug.adj[0]){
int w = e.to();
if(!marked[w]){
marked[w] = true;
parent[w] = 0;
dfs0(w);
/*根顶点相连的边是否是桥*/
if(low[w] > dfn[0]){
listE.add(new int[]{0, w});
}
childTree++;
}
}
/*单独处理根顶点*/
if(childTree >= 2){/*根顶点是割点的条件*/
isCutVer[0] = true;
}
}

/*除了根顶点的其它情况*/
  private void dfs0(int v){
    dfn[v] = low[v] = ++visitOrder;
for(Edge e : ug.adj[v]){
int w = e.to();
if(!marked[w]){
marked[w] = true;
parent[w] = v;
dfs0(w);
low[v] = Math.min(low[v], low[w]);

/*判断割点*/
if(low[w] >= dfn[v]){
isCutVer[v] = true;
/*判断桥*/
if(low[w] > dfn[v]){
listE.add(new int[]{v, w});
}
}
}else
if(parent[v] != w && dfn[w] < dfn[v]){
low[v] = Math.min(low[v], dfn[w]);
}
}
}

/*返回所有割点*/
  public List<Integer> allCutVer(){
for(int i = 0; i < isCutVer.length; i++){
    if(isCutVer[i]){
    listV.add(i);
    }
}
return listV;
}

/*返回所有割边*/
  public List<int[]> allCutEdge(){
return listE;
}

/*判断顶点v是否是割点*/
  public boolean isCutVer(int v){
return isCutVer[v];
}

public static void main(String[] args) throws FileNotFoundException{

File path = new File(System.getProperties()
                     .getProperty("user.dir"))
.getParentFile();

File f = new File(path, "algs4-data/tinyG2.txt");
FileReader fr = new FileReader(f);

UndirectedGraph ug = new UndirectedGraph(fr);
System.out.println("\n-------图的邻接表示法-------");
System.out.println(ug);

System.out.println("\n-------图中的割点-------");

CutVerEdge cve = new CutVerEdge(ug);
for(int i : cve.allCutVer()){
System.out.println(i);
}

System.out.println("\n-------图中的割边-----");

for(int[] a : cve.allCutEdge()){
System.out.println(a[0]+"  "+ a[1]);
}
}
}