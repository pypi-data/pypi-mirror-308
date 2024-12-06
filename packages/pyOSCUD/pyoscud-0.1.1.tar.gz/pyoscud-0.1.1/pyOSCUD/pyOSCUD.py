import itertools
from pulp import *
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import matplotlib.patches as mpatches
import plotly.graph_objects as go
from math import *
import networkx as nx
import copy


# This class likely represents a single-machine scheduling problem.
class SingleMachineSP:
    """
    SingleMachineSP (Single Machine Scheduling Problem): this class implements the Single Machine Scheduling Problem. We define a simple problem like 1||gamma. We implement dispatching rules and some algorithms to solve the problem. specific problems. We developed specific functions to describe the solution, compute the objective function(gamma) and plot the gantt chart.

    Attributes:
      Mandatory attributes:
        n: number of jobs
        J: set of jobs
        p: processing time of job j
      Optional attributes:
        m: number of machines
        M: set of machines
        d: due date of job j
        r: release date of job j
        w: weight of job j
        w1: weight associated for earliness of job j
        w2: weight associated for tardiness of job j
        sj: setup time of job j
        sijk: setup time dependent of sequence
        start: starting time of schedule
        objective: objective function
        gantt: if Yes the gantt is plotted
        verbose: if Yes main computations are shown
      Variables and computations:
        S: starting time of job j
        C: completion time of job j
        L: lateness of job j
        T: tardiness of job j
        E: earliness of job j
        U: penalty unit of job j
        Tmax: maximum tardiness
        Emax: maximum earliness
        Cmax: makespan or maximum completion time of all jobs
        Sumsijk: the total setup time
        objectiveFunction: objective function of the optimization model
        problemSP: name of the optimization model
        x: decision variable, starting time of job j in the machine i
        c:decision variable, completion time of job j
        cmax: decision variable,makespan
        y: decision variable, 1 if a job v precedes a job q in the machine i,
          0 otherwise
        f0: makespan objective function
        f1: average of completion time objective function
        f2: average of earliness objective function
        f3: average of tardiness objective function
        f4: total of late jobs objective function
        f5: weighted completion time objective function
        f6: weighted tardiness objective function
        f7: weighted earliness objective function
        f8: weighted tardiness and earliness objective function
        f9: maximum tardiness objective function
        f10: maximum earliness objective function
    """
    def __init__(self, n ,J , p, m = 1, prec = {}, M = {}, d = {}, r ={},w = {}, w1 = {},
                w2 = {}, sj = {}, sijk = {}, start = 0, objective = None,
                gantt = False, verbose = False):
        """

        Args:
          Mandatory attributes:
            n: number of jobs
            J: set of jobs
            p: processing time of job j
          Optional attributes:
            m: number of machines
            M: set of machines
            d: due date of job j
            r: release date of job j
            w: weight of job j
            w1: weight associated for earliness of job j
            w2: weight associated for tardiness of job j
            sj: setup time of job j
            sijk: setup time dependent of sequence
            start: starting time of schedule
            objective: Objective function
            gantt: if Yes the gantt is plotted
            verbose: if Yes main computations are shown
        """
        self.n = n
        self.J = J
        self.p = p
        self.m = m
        if prec == {}:
          self.prec = {j:0 for j in self.J}
          self.preced=False
        else:
          self.prec=prec
          self.G = nx.DiGraph(list(self.prec))
          if (set(self.J-self.G.nodes()))!=[]:
            for j in (set(self.J-self.G.nodes())):
              self.G.add_node(j)
          self.preced=True
        self.M = ['M1'] if M == {} else M
        self.d = {j:0 for j in self.J} if d == {} else d
        self.r = {j:0 for j in self.J} if r == {} else r
        self.w = {j:1 for j in self.J} if w == {} else w
        self.w1 = {j:1 for j in self.J} if w1 == {} else w1
        self.w2 = {j:1 for j in self.J} if w2 == {} else w2
        self.sj = {j:0 for j in self.J} if sj == {} else sj
        self.sijk = {i:{j:0 for j in self.J} for i in self.J} if sijk == {} else sijk
        self.start = start
        self.objective=objective
        self.gantt = gantt
        self.verbose = verbose
        self.S =  {j: 0 for j in self.J}
        self.C =  {j: 0 for j in self.J}
        self.L =  {j: 0 for j in self.J}
        self.T =  {j: 0 for j in self.J}
        self.E =  {j: 0 for j in self.J}
        self.U =  {j: 0 for j in self.J}
        self.Tmax=0
        self.Emax=0
        self.Cmax=0
        self.Sumsijk=0

    def visualize_Graph(self,results):
      """
        Create a chart to see a graph with precedence relations and the solution.
        Args:
          results:  is an array with the results of the schedule generation or
          optimization model

        Returns: the gantt chart

        """
#      self.G= nx.DiGraph(list(self.prec))
      
      
      schedule = pd.DataFrame(results)
      JOBS = sorted(list(schedule['Job'].unique()))
      MACHINES = sorted(list(schedule['Machine'].unique()))
      MA=list(schedule['Machine'])
      JO=list(schedule['Job'])
      MA={JO[j]:self.M.index(MA[j])+1 for j in range(self.n)}
      for layer, nodes in enumerate(nx.topological_generations(self.G)):
          for node in nodes:
              self.G.nodes[node]["layer"] = layer
      ColorLegend = {MACHINES[i]: i+1 for i in range(self.m)}
      values = [MA.get(node, 0) for node in self.G.nodes()]
      jet = cm = plt.get_cmap('jet')
      cNorm  = colors.Normalize(vmin=0, vmax=max(values))
      scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
      pos = nx.multipartite_layout(self.G, subset_key="layer")
      fig = plt.figure(1)
      ax = fig.add_subplot(1,1,1)
      for label in ColorLegend:
        ax.plot([0],[0],color=scalarMap.to_rgba(ColorLegend[label]),label=label)
      nx.draw_networkx(self.G,pos, cmap = jet, vmin=0, vmax= max(values),node_color=values,with_labels=True,ax=ax)
      ax.set_title("Graph of precedences")
      plt.axis('off')
      fig.set_facecolor('w')
      plt.legend()
      fig.tight_layout()
      return plt.show()

    def visualize(self,results):  
        """
        Create a gantt chart.
        Args:
          results:  is an array with the results of the schedule generation or
          optimization model

        Returns: the gantt chart

        """

        schedule = pd.DataFrame(results)
        JOBS = sorted(list(schedule['Job'].unique()))
        MACHINES = sorted(list(schedule['Machine'].unique()))
        makespan = schedule['Finish'].max()
        bar_style = {'alpha':1.0, 'lw':25, 'solid_capstyle':'butt'}
        text_style = {'color':'white', 'weight':'bold', 'ha':'center', 'va':'center'}
        colors = plt.cm.tab20.colors
        schedule.sort_values(by=['Job', 'Start'])
        schedule.set_index(['Job', 'Machine'], inplace=True)
        fig, ax = plt.subplots(2,1, figsize=(12, 5+(len(JOBS)+len(MACHINES))/4))
        for jdx, j in enumerate(JOBS, 1):
            for mdx, m in enumerate(MACHINES, 1):
                if (j,m) in schedule.index:
                    xs = schedule.loc[(j,m), 'Start']
                    xf = schedule.loc[(j,m), 'Finish']
                    ax[0].plot([xs, xf], [jdx]*2, c=colors[mdx%len(colors)], **bar_style)
                    ax[0].text((xs + xf)/2, jdx, m, **text_style)
                    ax[1].plot([xs, xf], [mdx]*2, c=colors[jdx%len(colors)], **bar_style)
                    ax[1].text((xs + xf)/2, mdx, j, **text_style)
        ax[0].set_title('Job Schedule')
        ax[0].set_ylabel('Job')
        ax[1].set_title('Machine Schedule')
        ax[1].set_ylabel('Machine')
        for idx, s in enumerate([JOBS, MACHINES]):
            ax[idx].set_ylim(0.5, len(s) + 0.5)
            ax[idx].set_yticks(range(1, 1 + len(s)))
            ax[idx].set_yticklabels(s)
            ax[idx].plot([makespan]*2, ax[idx].get_ylim(), 'r--',label=f"Cmax = {makespan}")
            ax[idx].set_xlabel('Time')
            ax[idx].grid(True)
        fig.tight_layout()
        red_patch = mpatches.Patch(color='red',fill='',linestyle='--', label=f"Cmax = {makespan}")
        fig.legend(handles=[red_patch],loc='lower right')
        return plt.show()

    def process(self,Sequence):
      """
      The function processes a sequence of jobs to be scheduled and calculates various metrics for
      each job.
      
      Args:
        Sequence: The `Sequence` parameter in the provided code snippet represents a sequence of
        jobs to be scheduled. It is an input to the `process` method of a class, where the scheduling
        computations are performed based on the given sequence of jobs
        
      return: The `process` method is returning an array `results` containing the computations of the
      schedule for the given sequence of jobs. The computations include details such as job start
      time, setup time, duration, finish time, due date, earliness, and tardiness for each job on each
      machine. Additionally, if the `verbose` flag is set to True, it prints the schedule by machine,
      and by jobs.
      """
      self.S =  {j: 0 for j in self.J}
      self.C =  {j: 0 for j in self.J}
      self.L =  {j: 0 for j in self.J}
      self.T =  {j: 0 for j in self.J}
      self.E =  {j: 0 for j in self.J}
      self.U =  {j: 0 for j in self.J}
      self.Tmax=0
      self.Emax=0
      self.Cmax=0
      self.Sumsijk=0

      self.Sumsijk=0
      for v in range(self.n):
          j = Sequence[v]
          js = Sequence[0] if v == self.n-1 else Sequence[v+1]
          if v==0:
            self.S[j] = max(self.r[j],self.start)
          else:
            self.S[j] = max(self.r[j], self.C[j1],self.start)
          self.C[j] = self.sj[j]+self.sijk[j][js] + self.S[j] + self.p[j]
          self.L[j] = self.C[j] - self.d[j]
          self.T[j] = max(0, self.L[j])
          self.E[j] = max(0, -self.L[j])
          if self.T[j]>0: self.U[j] = 1
          self.Sumsijk+=self.sijk[j][js]
          j1=j
      results = [{'Job': j,'Machine': self.M[i],'Start': self.S[j],
                  'Setup' : self.C[j]-self.p[j]-self.S[j],
                  'Duration': self.p[j], 'Finish': self.C[j],
                  'Due': self.d[j],'earliness': self.E[j],
                  'Tardiness': self.T[j]} for j in Sequence
                for i in range(self.m)]
      schedule = pd.DataFrame(results)
      if self.verbose == True:
        print('\nSchedule by Machine')
        print(schedule.sort_values(by=['Machine','Start']).set_index(['Machine', 'Job']))
      if self.gantt==True:
        self.visualize(results)
      self.compute_objective(self.objective)
      return results

    def showResults(self,Sequence):
      """
      The function `showResults` takes a sequence of jobs to be scheduled, processes them, and
      visualizes the results if the `gantt` attribute is set to `True`.
      Args:
        Sequence: The `Sequence` parameter in the `showResults` method is a sequence of jobs that
        need to be scheduled. This sequence will be processed and the results will be visualized if the
        `gantt` attribute is set to `True`
      """

      self.verbose = True
      results = self.process(Sequence)
      self.verbose = False
      if self.gantt==True:
        self.visualize(results)


    def set_start(self, start):
        """

        Args:
          start: starting time of schedule
        """
        self.start = start

    def set_sequence(self,seq):
        """

        Args:
          seq: Sequence of jobs to be scheduled

        Returns: Sequence

        """
        Sequence=seq
        self.process(Sequence)
        return Sequence

    def compute_objective(self, objective):
        """

      Args:
        objective: objective function to evaluate

      Returns: objective value

      """
        obj=0
        if objective == "AvgC":
          obj=sum(self.C.values())/self.n
          print("AvgC=",obj)
        if objective == "AvgE":
          obj=sum(self.E.values())/self.n
          print("AvgE=",obj)
        if objective == "AvgT":
          obj=sum(self.T.values())/self.n
          print("AvgT=",obj)
        if objective == "MinTotalLateJobs":
          obj=sum(self.U.values())
          print("MinTotalLateJobs=",obj)
        if objective == "WeightedC":
          obj = sum(w * c for w, c in zip(self.w.values(), self.C.values()))
          print("WeightedC=",obj)
        if objective == "WeightedT":
          obj = sum(w * t for w, t in zip(self.w.values(), self.T.values()))
          print("WeightedT=",obj)
        if objective == "WeightedE":
          obj=sum(w * e for w, e in zip(self.w.values(), self.E.values()))
          print("WeightedE=",obj)
        if objective == "WeightedT+E":
          obj = sum(w * t for w, t in zip(self.w2.values(), self.T.values())) + sum(w * e for w, e in zip(self.w1.values(),self.E.values()))
          print("WeightedT+E=",obj)
        if objective == "Tmax":
          obj=max(self.T.values())
          print("Tmax=",obj)
        if objective == "Emax":
          obj=max(self.E.values())
          print("Emax=",obj)
        if objective == "Cmax":
          obj=max(self.C.values())
          print("Cmax=",obj)
        if objective == "Lmax":
          obj=max(self.L.values())
          print("Lmax=",obj)
        if objective == "sijk":
          obj=self.Sumsijk
          print("Sum of sijk=",obj)
        if objective is None:
          obj=[]
          obj.append(sum(self.C.values())/self.n)
          print("AvgC=",obj)
          obj.append(sum(self.E.values())/self.n)
          print("AvgE=",obj)
          obj.append(sum(self.T.values())/self.n)
          print("AvgT=",obj)
        return obj

    def FCFS(self):
        """
        FCFS (First Come First Serve) rule to schedule jobs.
        Returns: Sequence of jobs to be scheduled

        """
        if self.preced:
          Sequence=[]
          b = True
          G2=self.G.copy()
          while b:
            F=[ i for i in G2 if list(G2.predecessors(i))==[]]
            p1={j:self.p[j] for j in F}
            d1={j:self.d[j] for j in F}
            s=[x for _, x in sorted(zip(p1.values(), F))]
            G2.remove_nodes_from(F)
            if G2.number_of_nodes()==0:
              b=False
            Sequence=Sequence+s
        else:
          Sequence = self.J
        self.process(Sequence)
        return Sequence

    def RANDOM(self):
        """
        RANDOM rule to schedule jobs.
        Returns: Sequence of jobs to be scheduled

        """
        Sequence = random.sample(self.J,k=self.n)
        self.process(Sequence)
        return Sequence

    def LCFS(self):
        """
        LCFS (Last Come First Serve) rule to schedule jobs.
        Returns: Sequence of jobs to be scheduled

        """
        Sequence = self.J[::-1]
        self.process(Sequence)
        return Sequence

    FIFO = FCFS
    LIFO = LCFS

    def SPT(self):
        """
        SPT (Shortest Processing Time) rule to schedule jobs.
        Returns: Sequence of jobs to be scheduled

        """
        if self.preced:
          Sequence=[]
          b = True
          G2=self.G.copy()
          while b:
            F=[ i for i in G2 if list(G2.predecessors(i))==[]]
            p1={j:self.p[j] for j in F}
            d1={j:self.d[j] for j in F}
            s=[x for _, x in sorted(zip(p1.values(), F))]
            G2.remove_nodes_from(F)
            if G2.number_of_nodes()==0:
              b=False
            Sequence=Sequence+s
        else:
          Sequence = [x for _, x in sorted(zip(self.p.values(), self.J))]
        self.process(Sequence)
        return Sequence

    def LPT(self):
        """
        LPT (Longest Processing Time) rule to schedule jobs.
        Returns: Sequence of jobs to be scheduled

        """
        if self.preced:
          Sequence=[]
          b = True
          G2=self.G.copy()
          while b:
            F=[ i for i in G2 if list(G2.predecessors(i))==[]]
            p1={j:self.p[j] for j in F}
            d1={j:self.d[j] for j in F}
            r1={j:self.r[j] for j in F}
            s=[x for _, x in sorted(zip(zip(r1.values(),[-k for k in p1.values()]), F))]
            G2.remove_nodes_from(F)
            if G2.number_of_nodes()==0:
              b=False
            Sequence=Sequence+s
        else:
          Sequence = [x for _, x in sorted(zip(zip(self.r.values(),[-k for k in self.p.values()]), self.J))]
        self.process(Sequence)
        return Sequence

    def WSPT(self):
        """
        WSPT (Weighted Shortest Processing Time) rule to schedule jobs.
        Returns: Sequence of jobs to be scheduled

        """
        rs = [x/y for x, y in zip(self.p.values(), self.w.values())]
        Sequence = [x for _, x in sorted(zip(zip(self.r.values(), rs), self.J))]
        self.process(Sequence)
        return Sequence

    def WLPT(self):
        """
        WLPT (Weighted Longest Processing Time) rule to schedule jobs.
        Returns: Sequence of jobs to be scheduled

        """
        rs = [x/y for x, y in zip(self.p.values(), self.w.values())]
        Sequence = [x for _, x in sorted(zip(zip(self.r.values(), [-k for k in rs]), self.J))]
        self.process(Sequence)
        return Sequence

    def EDD(self):
        """
        EDD (Earliest Due Date) rule to schedule jobs.
        Returns: Sequence of jobs to be scheduled

        """
        if self.preced:
          Sequence=[]
          b = True
          G2=self.G.copy()
          while b:
            F=[ i for i in G2 if list(G2.predecessors(i))==[]]
            p1={j:self.p[j] for j in F}
            d1={j:self.d[j] for j in F}
            r1={j:self.r[j] for j in F}
            s=[x for _, x in sorted(zip(zip(r1.values(),d1.values()), F))]
            G2.remove_nodes_from(F)
            if G2.number_of_nodes()==0:
              b=False
            Sequence=Sequence+s
        else:
          Sequence = [x for _, x in sorted(zip(zip(self.r.values(),self.d.values()), self.J))]
        self.process(Sequence)
        return Sequence

    def LDD(self):
        """
        LDD (Latest Due Date) rule to schedule jobs.
        Returns: Sequence of jobs to be scheduled

        """
        if self.preced:
          Sequence=[]
          b = True
          G2=self.G.copy()
          while b:
            F=[ i for i in G2 if list(G2.predecessors(i))==[]]
            p1={j:self.p[j] for j in F}
            d1={j:self.d[j] for j in F}
            r1={j:self.r[j] for j in F}
            s=[x for _, x in sorted(zip(zip(r1.values(),[-k for k in d1.values()]), F))]
            G2.remove_nodes_from(F)
            if G2.number_of_nodes()==0:
              b=False
            Sequence=Sequence+s
        else:
          Sequence = [x for _, x in sorted(zip(zip(self.r.values(),[-k for k in self.d.values()]), self.J))]
        self.process(Sequence)
        return Sequence

    def CR(self, check_time=False):
        """
        CR (Critical Ratio) rule to schedule jobs.
        Args:
          check_time: time to compute the CR.

        Returns: Sequence of jobs to be scheduled

        """

        if check_time == False:
            SyntaxError("check_time is not defined, Start time is used instead")
            check_time = self.start
        t = check_time
        print(t)
        CR = [(a-t)/b for a,b in zip(self.d.values(), self.p.values())]
        Sequence = [x for _, x in sorted(zip(CR, self.J))]
        self.process(Sequence)
        return Sequence
    CriticalRatio = CR

    def MinimumSlack(self, check_time=False):
        """
        Minimum Slack rule to schedule jobs.
        Args:
          check_time: time to compute the Minimum Slack.

        Returns: Sequence of jobs to be scheduled

        """
        if check_time == False:
            SyntaxError("check_time is not defined, Start time is used instead")
            check_time = self.start
        t = check_time
        MS = [max(0,(a-t-b)) for a,b in zip(self.d.values(), self.p.values())]
        Sequence = [x for _, x in sorted(zip(MS, self.J))]
        self.process(Sequence)
        return Sequence
    MinSlack = MinimumSlack

    def MaximumSlack(self, check_time=False):
        """
        Maximum Slack rule to schedule jobs.
        Args:
          check_time: time to compute the Maximum Slack.

        Returns: Sequence of jobs to be scheduled

        """

        if check_time == False:
            SyntaxError("check_time is not defined, Start time is used instead")
            check_time = self.start
        t = check_time
        MS = [max(0,(b-t-a)) for a,b in zip(self.d.values(), self.p.values())]
        Sequence = [x for _, x in sorted(zip(MS, self.J), reverse=True)]
        self.process(Sequence)
        return Sequence
    MaxSlack = MaximumSlack

    def ATC(self, check_time=False, K =False):
        """
        ATC (Apparent Tardiness Cost) rule to schedule jobs.
        Args:
          check_time: time to compute the ATC.
          K: constant to compute the ATC. if K=False, 1 is used

        Returns: Sequence of jobs to be scheduled

        """

        if check_time == False:
            SyntaxError("check_time is not defined, Start time is used instead")
            check_time = self.start
        if K == False:
            SyntaxError("K is not defined, K = 1 is used instead")
            K = 1
        t = check_time
        ATC = [0]*self.n
        P = sum(self.p.values())/self.n
        ATC=[(a/b)*exp(-max(c-t-b, 0)/(K*P)) for  a,b,c in zip(self.w.values(), self.p.values(),self.d.values())]
        Sequence = [x for _, x in sorted(zip(ATC, self.J), reverse=True)]
        self.process(Sequence)
        return Sequence

    def CommonDueDate(self):
        """
        Common Due Date algorithm to schedule jobs.
        Returns: Sequence of jobs to be scheduled

        """

        if len(set(self.d)) != 1:
            SyntaxError("Not All jobs have the same due date")
        #Step 0: Rank the jobs in SPT order
        seq=self.SPT()
        #Step 1: Create two sets A and B
        A = []
        B = []
        #Step 2: Compute Cmax = \sum_{j=1}^{n} p_j, i = n, R = Cmax-d
        n = self.n
        Cmax = sum(self.p.values())
        i = n-1
        R = Cmax - self.d[seq[i]]
        L = self.d[seq[i]]
        #Step 3: If R > L, then add job i to set A and go to step 4
        while i >= 0:
            #print(R," ", L)
            if R >= L:
                A.append(seq[i])
                R = R-self.p[seq[i]]
                        #print("A ",A)
            else:
                B.append(seq[i])
                L = L-self.p[seq[i]]
                        #print("B", B)
            i -= 1
        Sequence = B + list(reversed(A))
        self.process(Sequence)
        print("Obj = ",sum(self.E.values())+sum(self.T.values()))
        return Sequence

    def DifferentDueDates(self, groups = [],  P1: float = 1, P2: float = 1, P3: float = 1):
        """
        Different Due Dates algorithm to schedule jobs.
        Args:
          groups: size of groups to be scheduled
          P1: Cost of due date.
          P2: Penalty for early jobs
          P3: Penalty for late jobs

        Returns: Sequence of jobs to be scheduled

        """
        if len(set(self.d)) == 1:
            SyntaxError("All jobs have the same due date, Common Due Date is recommended instead")
        #Step 1: Rank the jobs in SPT order
        self.SPT()
        #Step 2: Set N[0] = 0, N[j] = sum_{k=1}^j n_k, j = 1,2,...,n
        mg = len(groups)
        N = [0]*(mg+1)
        k = [0]*(mg+1)
        N[0] = 0
        k[0] = 0
        for j in range(1,mg+1):
            N[j]=sum(groups[:j])
            k[j]=N[j-1]+ceil((groups[j-1]*(P3-P1)/(P3+P2)))
        delta=[0]*self.n
        for q in range(self.n):
          for j in range(1,mg+1):
            if q in range(N[j-1],k[j]):
              delta[q]=P2*(q+1-1-N[j-1])+P1*(self.n-N[j-1])
              break
            if q in range(k[j],N[j]):
              delta[q]=P3*(N[j]-q-1+1)+P1*(self.n-N[j])
              break
        seq = sorted(delta,reverse=True)
        index = [seq.index(v)+1 for v in delta]
        for j in range(self.n):
          if index.count(index[j]) != 1:
            index[j]+=1
        Order=[0]*self.n
        for j in range(self.n):
          Order[j]=self.J[index[j]-1]
        Sequence=Order
        obj = sum(self.p[Sequence[j]]*delta[j] for j in range(self.n))
        print("Objective value = ",obj)
        D=[0]*(mg+1)
        for i in range(1,mg+1):
          for j in range(k[i]):
            D[i]+=self.p[Sequence[j]]
        for j, i in itertools.product(range(self.n), range(1,mg+1)):
            if j in range(N[i-1],N[i]):
              self.d[Sequence[j]]=D[i]
        self.process(Sequence)
        print("Obj = ",P1*sum(self.d.values())+P2*sum(self.E.values())+
              P3*sum(self.T.values()))
        return Sequence

    def Moore(self):
        """
        Moore's algorithm to schedule jobs.

        Returns: Sequence of jobs to be scheduled

        """
        if len(set(self.d)) != 1:
            SyntaxError("Not All jobs have the same due date")
        #Step 0: Rank the jobs in EDD order
        seq=self.EDD()
        C1=self.C
        J1=[]
        Jd=[]
        t=0
        for k in seq:
            J1.append(k)
            t+=self.p[k]
            if t>self.d[k]:
              p2 = {m: self.p[m] for m in self.J if m in J1}
              ind=max(p2,key=p2.get)
              J1.remove(ind)
              t=t-self.p[ind]
              Jd.append(ind)
        Sequence=J1+Jd
        self.process(Sequence)
        print("Obj = ",len(Jd))
        return Sequence

    def lawler(self,prec):
        """
        Special case of Lawler's algorithm for minimizing maximum lateness
        where hj = Cj - dj

        Args:
          prec:dictionary with keys "Job" and values list of predecessors

        Returns: Sequence of jobs to be scheduled

        """
        # Initialize
        J0 = []
        JC = self.J.copy()
        G2=self.G.copy()
        # J_1 = Jobs with no predecessors
        J_1= [i for i in G2.nodes() if list(self.G.successors(i))==[]]
        # While there are jobs left in JC
        while JC:
            # Find the sum of all the processing times of the jobs in JC
            Cmax = sum([self.p[job] for job in JC])
            # Evaluate hj for all jobs in J_1
            h = [Cmax - self.d[job] for job in J_1]
            # Find the job with the minimum hj
            j = J_1[h.index(min(h))]
            #### Reevaluate J, JC, and J_1
            # Add j to be the first job in J
            J0.insert(0, j)
            # Remove j from JC
            JC.remove(j)
            # Delete all precedence constraints involving j
            for job in self.J:
                if j in prec[job]:
                    prec[job].remove(j)
            G2.remove_node(j)
            # J_1 = Jobs with no predecessors that are not in J
            J_1 = [i for i in G2.nodes() if list(G2.successors(i))==[] and i not in J0]
        Sequence=J0
        self.process(Sequence)
        print("Obj = ",max(self.L.values()))
        return Sequence

    def twoOpt(self,s):
        sol=s
        j = random.randint(0,len(sol)-1)
        k=random.randint(0,len(sol)-1)
        while (k==j):
          k=random.randint(0,len(sol)-1)
        a=sol[k]
        b=sol[j]
        sol[j]=a
        sol[k]=b
        return sol


    def decreaseT(self,t,decreaseMethod,alpha):
        if decreaseMethod=='Geometric':
          return alpha*t
        if decreaseMethod=='Lineal':
          return t-alpha

    def SA(self,s,MaxIter,TemIni,decreaseMethod='Geometric',alpha=0.98):
        """

        Args:
          s: initial solution
          MaxIter: maximum number of iterations
          TemIni: initial temperature
          decreaseMethod: method to decrease temperature
          alpha: parameter to decrease temperature

        Returns: Sequence of jobs to be scheduled

        """
        Best=s
        self.process(s)
        c1=self.compute_objective(self.objective)
        cb=self.compute_objective(self.objective)
        k=0
        t=TemIni
        Val=[[k,c1,cb,0,(t/1000),s,Best]]
        while (k<MaxIter):
            k += 1
            R=self.twoOpt(s)
            self.process(R)
            c2=self.compute_objective(self.objective)
            p=random.random()
            prob=[p,np.exp(-(c2-c1)/t)]
            if c2<c1 or p<np.exp(-(c2-c1)/t):
              s=R
              self.process(s)
              c1=self.compute_objective(self.objective)
            t=self.decreaseT(t,decreaseMethod,alpha);
            if c1<cb:
              Best=s.copy()
              self.process(Best)
              cb=self.compute_objective(self.objective)
            Val1=[k,c1,cb,prob[0],(t/1000),s,Best]
            #print(Val1)
            Val.append(Val1)
        #print(Best,cb)
        #print(s,c1)
        df=pd.DataFrame(Val)
        df
        x=df[0]
        y=df[1]
        plt.plot(x, y,linestyle='-')
        return Best

    def optimizationModel(self,problemName,objectiveFunction):
        """
        Create a optimization model to solve the scheduling problem.

        Args:
          problemName: name of the problem
          objectiveFunction: objective function to be minimized
        """
        self.objectiveFunction=objectiveFunction
        # Problem Definition
        self.problemSP=LpProblem(problemName,LpMinimize)
        #Decision Variables
        self.x=LpVariable.dicts('x',((j,i) for j in self.J for i in self.M),lowBound=0,cat='Continuous')
        self.c = LpVariable.dicts('c', iter(self.J), lowBound=0, cat='Continuous')
        self.E = LpVariable.dicts('E', iter(self.J), lowBound=0, cat='Continuous')
        self.T = LpVariable.dicts('T', iter(self.J), lowBound=0, cat='Continuous')
        self.U = LpVariable.dicts('U', iter(self.J), lowBound=0, cat='Binary')
        self.cmax=LpVariable('cmax',cat='Continuous')
        self.Tmax=LpVariable('Tmax',cat='Continuous')
        self.Emax=LpVariable('Emax',cat='Continuous')
        self.Lmax=LpVariable('Lmax',cat='Continuous')
        self.y=LpVariable.dicts('y',((u,v,i) for u in self.J for v in self.J for i in self.M),cat='Binary')
        # Objective functions
        self.f0=LpAffineExpression(self.cmax)
        self.f1=LpAffineExpression(lpSum(self.c[j] for j in self.J)/self.n)
        self.f2=LpAffineExpression(lpSum(self.E[j] for j in self.J)/self.n)
        self.f3=LpAffineExpression(lpSum(self.T[j] for j in self.J)/self.n)
        self.f4=LpAffineExpression(lpSum(self.U[j] for j in self.J))
        self.f5=LpAffineExpression(lpSum(self.w[j]*self.c[j] for j in self.J))
        self.f6=LpAffineExpression(lpSum(self.w[j]*self.T[j] for j in self.J))
        self.f7=LpAffineExpression(lpSum(self.w[j]*self.E[j] for j in self.J))
        self.f8=LpAffineExpression(lpSum((self.w1[j]*self.E[j]+self.w2[j]*self.T[j]) for j in self.J))
        self.f9=LpAffineExpression(self.Tmax)
        self.f10=LpAffineExpression(self.Emax)
        self.f11=LpAffineExpression(self.Lmax)
        
        if objectiveFunction =="Cmax":
          self.problemSP.setObjective(self.f0)
        if objectiveFunction == "AvgC":
          self.problemSP.setObjective(self.f1)
        if objectiveFunction == "AvgE":
          self.problemSP.setObjective(self.f2)
        if objectiveFunction == "AvgT":
          self.problemSP.setObjective(self.f3)
        if objectiveFunction == "MinTotalLateJobs":
          self.problemSP.setObjective(self.f4)
        if objectiveFunction == "WeightedC":
          self.problemSP.setObjective(self.f5)
        if objectiveFunction == "WeightedT":
          self.problemSP.setObjective(self.f6)
        if objectiveFunction == "WeightedE":
          self.problemSP.setObjective(self.f7)
        if objectiveFunction == "WeightedT+E":
          self.problemSP.setObjective(self.f8)
        if objectiveFunction == "Tmax":
          self.problemSP.setObjective(self.f9)
        if objectiveFunction == "Emax":
          self.problemSP.setObjective(self.f10)
        if objectiveFunction == "Lmax":
          self.problemSP.setObjective(self.f11)
        if objectiveFunction is None:
          print("No objective defined, the makespan will be minimized")
          self.problemSP.setObjective(self.f0)
        MM=sum(self.p.values())*100
        #earliness and tardiness constraints
        for j in self.J:
          self.problemSP+=self.c[j]==self.d[j]+self.T[j]-self.E[j],'EYT'+j
          self.problemSP+=self.T[j]<=self.U[j]*MM,'U'+j
          self.problemSP+=self.E[j]<=self.Emax
          self.problemSP+=self.T[j]<=self.Tmax
          self.problemSP+=self.T[j]-self.E[j]<=self.Lmax          
        # ending constraints
        for i in self.M:
          for j in self.J:
            self.problemSP+=self.x[j,i]+self.p[j]==self.c[j]
        #non-interference constraints
        for i in self.M:
          for u in self.J:
            for v in self.J:
              if (u!=v):
                self.problemSP+=self.x[v,i]-self.x[u,i]+MM*(1-self.y[u,v,i])>=self.p[u]+self.sj[u]+self.sijk[u][v]
                self.problemSP+=self.x[u,i]-self.x[v,i]+MM*(self.y[u,v,i])>=self.p[v]+self.sj[v]+self.sijk[v][u]
        # precedence-constraints
        if self.preced==True:
          for (u,v) in self.prec:
            for i in self.M:
              self.problemSP+=self.y[u,v,i]==1

    def showModel(self,filename):
          """

          Args:
            filename: name of file to write the model
          """
          self.problemSP.writeLP(filename)

    def solve(self):
          """
          solve the optimization problem
          Returns: array with the solution

          """
          self.problemSP.solve()
          print ("Status: ",LpStatus[self.problemSP.status])
          print("Objective Function (",self.objectiveFunction,") = ",self.problemSP.objective.value())
          results = [{'Job': j,'Machine': i,'Start': value(self.x[j,i]),'Duration': self.p[j], 'Finish': value(self.c[j]), 'Due': self.d[j],'earliness': value(self.E[j]),'Tardiness': value(self.T[j])} for j in self.J for i in self.M]
          schedule = pd.DataFrame(results)
          print('\nSchedule by Job')
          print(schedule.sort_values(by=['Job','Start']).set_index(['Job', 'Machine']))
          print('\nSchedule by Machine')
          print(schedule.sort_values(by=['Machine','Start']).set_index(['Machine', 'Job']))
          return results


class MultiMachineSP:
    """
    MultiMachineSP (Multi Machine Scheduling Problem) Class: this class implements the Multi Machine Scheduling Problem. We define a simple problem like alpha||gamma. We implement dispatching rules and some algorithms to solve the problem specific problems. This class supports Flow Shop, Job Shop and Open Shop. We developed specific functions to describe the solution, compute the Objective function(gamma) and plot the gantt chart.

    Attributes:
    Mandatory Attributes:
      n: number of jobs
      m: number of machines
      J: set of jobs
      M: set of machines
      p: processing time
      ty: type of scheduling
    Optional args:
      prec: precedence
      preced: if True, precedences is active, False otherwise
      G: graph of precedences
      d: due date
      r: release date
      w: weight
      w1: weight for late jobs
      w2: weight for tardiness
      O: set of machines for each job
      sijk: setup time dependent of sequence
      start: starting time
      objective: objective function
      gantt: if True, show Gantt chart
      verbose: if True, show results: due date
    Variables and computations:
      S: start time for job j
      CC: completion time for job j
      C: completion time for job j
      L: lateness for job j
      T: tardiness for job j
      E: earliness for job j
      U: unit penalty of job j or Late job
      Tmax: maximum tardiness
      Emax: maximum earliness
      Cmax: makespan
    Decision variables for the optimization problem:
      objectiveFunction: objective function
      problemSP: name of the problem
      x: decision variable - starting time for each job in each machine
      y: decision variable - 1 if a job q precedes a job p in the sequence in machine i, 0 otherwise
      c: decision variable - completion time of each job in each machine
      cmax:decision variables-  makespan
      f0: makespan objective function
      f1: average of completion time objective function
      f2: average of earliness objective function
      f3: average of tardiness objective function
      f4: total of late jobs objective function
      f5: weighted completion time objective function
      f6: weighted tardiness objective function
      f7: weighted earliness objective function
      f8: weighted tardiness and earliness objective function
      f9: maximum tardiness objective function
      f10: maximum earliness objective function:
    """
    def __init__(self, n ,m , J, M, p, ty, prec = {},d = {}, r = {}, w = {}, w1 = {}, w2 = {}, O = {}, sijk = {},start = 0, objective = 0, gantt = False, verbose = False):
        """

        Args:
        Mandatory args:
          n: number of jobs
          m: number of machines
          J: set of jobs
          M: set of machines
          p: processing time
          ty: type of scheduling
        Optional args:
          prec: precedence
          preced: if True, precedences is active, False otherwise
          G: graph of precedences
          d: due date
          r: release date
          w: weight
          w1: weight for late jobs
          w2: weight for tardiness
          O: set of machines for each job
          sijk: setup time dependent of sequence
          start: starting time
          objective: objective function
          gantt: if True, show Gantt chart
          verbose: if True, show results

        """

        #Input Data
        self.n = n
        self.m = m
        self.J = J
        self.M = M
        self.p = p
        self.ty=ty
        if prec == {}:
          self.prec = {j:0 for j in self.J}
          self.preced=False
        else:
          self.prec=prec
          self.G = nx.DiGraph(list(self.prec))
          if (set(self.J-self.G.nodes()))!=[]:
            for j in (set(self.J-self.G.nodes())):
              self.G.add_node(j)          
          self.preced=True
        self.d = {j:0 for j in self.J} if d == {} else d
        self.r = {j:0 for j in self.J} if r == {} else r
        self.w = {j:1 for j in self.J} if w == {} else w
        self.w1 = {j:1 for j in self.J} if w1 == {} else w1
        self.w2 = {j:1 for j in self.J} if w2 == {} else w2
        if O == {}:
          self.O = {j:{i:self.M[i] for i in range(self.m)} for j in self.J}
        else:
          self.O=O
        self.sijk = {i:{j:0 for j in self.J} for i in self.J} if sijk == {} else sijk
        self.start = start
        self.objective=objective
        self.gantt = gantt
        self.verbose = verbose
        #Computations
        self.S =  {j: {i: 0 for i in self.M} for j in self.J}
        self.CC =  {j: {i: 0 for i in self.M} for j in self.J}
        self.C =  {j: 0 for j in self.J}
        self.L =  {j: 0 for j in self.J}
        self.T =  {j: 0 for j in self.J}
        self.E =  {j: 0 for j in self.J}
        self.U =  {j: 0 for j in self.J}
        self.Tmax=0
        self.Emax=0
        self.Cmax=0


    def visualize(self,results):
        """
        Create a gantt chart.
        Args:
          results:  is an array with the results of the schedule generation or
          optimization model

        Returns: the gantt chart
        """
        schedule = pd.DataFrame(results)
        JOBS = sorted(list(schedule['Job'].unique()))
        MACHINES = sorted(list(schedule['Machine'].unique()))
        makespan = schedule['Finish'].max()
        bar_style = {'alpha':1.0, 'lw':25, 'solid_capstyle':'butt'}
        text_style = {'color':'white', 'weight':'bold', 'ha':'center', 'va':'center'}
        colors = plt.cm.tab20.colors
        schedule.sort_values(by=['Job', 'Start'])
        schedule.set_index(['Job', 'Machine'], inplace=True)
        fig, ax = plt.subplots(2,1, figsize=(12, 5+(len(JOBS)+len(MACHINES))/4))
        for jdx, j in enumerate(JOBS, 1):
            for mdx, m in enumerate(MACHINES, 1):
                if (j,m) in schedule.index:
                    xs = schedule.loc[(j,m), 'Start']
                    xf = schedule.loc[(j,m), 'Finish']
                    ax[0].plot([xs, xf], [jdx]*2, c=colors[mdx%len(colors)], **bar_style)
                    ax[0].text((xs + xf)/2, jdx, m, **text_style)
                    ax[1].plot([xs, xf], [mdx]*2, c=colors[jdx%len(colors)], **bar_style)
                    ax[1].text((xs + xf)/2, mdx, j, **text_style)
        ax[0].set_title('Job Schedule')
        ax[0].set_ylabel('Job')
        ax[1].set_title('Machine Schedule')
        ax[1].set_ylabel('Machine')
        for idx, s in enumerate([JOBS, MACHINES]):
            ax[idx].set_ylim(0.5, len(s) + 0.5)
            ax[idx].set_yticks(range(1, 1 + len(s)))
            ax[idx].set_yticklabels(s)
            #ax[idx].text(makespan, ax[idx].get_ylim()[0]-0.2, "{0:0.1f}".format(makespan), ha='center', va='top')
            ax[idx].plot([makespan]*2, ax[idx].get_ylim(), 'r--')
            ax[idx].set_xlabel('Time')
            ax[idx].grid(True)
        fig.tight_layout()
        red_patch = mpatches.Patch(color='red',fill='',linestyle='--', label=f"Cmax = {makespan}")
        fig.legend(handles=[red_patch],loc='lower right')

        return plt.show()

    def visualize_Graph(self,results):
      """
        Create a chart to see a graph with precedence relations and the solution.
        Args:
          results:  is an array with the results of the schedule generation or
          optimization model

        Returns: the gantt chart

        """
      self.G= nx.DiGraph(list(self.prec))
      schedule = pd.DataFrame(results)
      JOBS = sorted(list(schedule['Job'].unique()))
      MACHINES = sorted(list(schedule['Machine'].unique()))
      MA=list(schedule['Machine'])
      JO=list(schedule['Job'])
      MA={JO[j]:self.M.index(MA[j])+1 for j in range(self.n)}
      for layer, nodes in enumerate(nx.topological_generations(self.G)):
          for node in nodes:
              self.G.nodes[node]["layer"] = layer
      ColorLegend = {MACHINES[i]: i+1 for i in range(self.m)}
      values = [MA.get(node, 0) for node in self.G.nodes()]
      jet = cm = plt.get_cmap('jet')
      cNorm  = colors.Normalize(vmin=0, vmax=max(values))
      scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
      pos = nx.multipartite_layout(self.G, subset_key="layer")
      fig = plt.figure(1)
      ax = fig.add_subplot(1,1,1)
      nx.draw_networkx(self.G,pos, cmap = jet, vmin=0, vmax= max(values),with_labels=True,ax=ax)
      ax.set_title("Graph of precedences")
      plt.axis('off')
      fig.set_facecolor('w')
      fig.tight_layout()
      return plt.show()


    def process(self,Sequence,sequenceMach={},optimum=False):
        """

        Args:
          Sequence: Sequence of jobs
          sequenceMach: Sequence of machines for each job
          optimum: if True, compute optimum solution

        Returns: results (array  with the computations of the schedule)

        """
        if self.ty=="Flow-Shop":
          CM =  {i: 0 for i in self.M}
          for v in range(self.n):
            j = Sequence[v]
            if v == 0:
              for q in range(len(self.O[j])):
                i = self.O[j][q]
                if q == 0:
                  self.S[j][i] = max(self.r[j], self.start,CM[i])
                else:
                  self.S[j][i] = self.CC[j][iant]
                self.CC[j][i] = self.S[j][i] + self.p[j][i]
                iant=i
                CM[i] = self.CC[j][i]
              jant=j
            else:
              for q in range(len(self.O[j])):
                i = self.O[j][q]
                if q == 0:
                  self.S[j][i] = max(self.r[j], self.start,self.CC[jant][i],CM[i])
                else:
                  self.S[j][i] = max(self.CC[j][iant], self.CC[jant][i],CM[i])
                self.CC[j][i] = self.S[j][i] + self.p[j][i]
                iant=i
                CM[i] = self.CC[j][i]
              jant=j
            self.C[j] = self.CC[j][i]
            self.L[j] = self.C[j] - self.d[j]
            self.T[j] = max(0, self.L[j])
            self.E[j] = max(0, -self.L[j])
            if self.T[j]>0: self.U[j] = 1
          results = [{'Job': j,'Machine': self.O[j][i],'Start': self.S[j][self.O[j][i]],'Duration': self.p[j][self.O[j][i]], 'Finish': self.CC[j][self.O[j][i]], 'Due':self.d[j], 'earliness': self.E[j], 'Tardiness': self.T[j]} for j in self.J for i in range(len(self.O[j]))]
          schedule = pd.DataFrame(results)
        if (self.ty=="Job-Shop"):
          CM =  {i: 0 for i in self.M}
          CJ =  {j: 0 for j in self.J}
          ONum=[len(self.O[j]) for j in self.J]
          pok = False
          for q in range(max(ONum)):
            for v in range(self.n):
              j = Sequence[v]
              if v == 0 and pok == False:
                pok = True
                if (q<len(self.O[j])):
                  i = self.O[j][q]
                  if q == 0:
                    self.S[j][i] = max(self.r[j], self.start,CM[i])
                  else:
                    self.S[j][i] = max(CM[i],CJ[j])
                  self.CC[j][i] = self.S[j][i] + self.p[j][i]
                  iant=i
                  CM[i] = self.CC[j][i]
                CJ[j] = self.CC[j][i]
                jant=j
              else:
                if (q<len(self.O[j])):
                  i = self.O[j][q]
                  if q == 0:
                    self.S[j][i] = max(self.r[j], self.start,CM[i])
                  else:
                    self.S[j][i] = max(CM[i],CJ[j])
                  self.CC[j][i] = self.S[j][i] + self.p[j][i]
                  iant=i
                  CM[i] = self.CC[j][i]
                CJ[j] = self.CC[j][i]
                jant=j
          for j in self.J:
            q = self.O[j][len(self.O[j])-1]
            self.C[j] = self.CC[j][q]
            self.L[j] = self.C[j] - self.d[j]
            self.T[j] = max(0, self.L[j])
            self.E[j] = max(0, -self.L[j])
            if self.T[j]>0: self.U[j] = 1
          results = [{'Job': j,'Machine': self.O[j][i],'Start': self.S[j][self.O[j][i]],'Duration': self.p[j][self.O[j][i]], 'Finish': self.CC[j][self.O[j][i]], 'Due':self.d[j], 'earliness': self.E[j], 'Tardiness': self.T[j]} for j in self.J for i in range(len(self.O[j]))]
          schedule = pd.DataFrame(results)
        if (self.ty=="Open-Shop" and optimum==False):
          machines=[0 for i in range(self.m)]
          jobs_list=[[] for i in range(self.m)]
          mac_list={j:[] for j in self.J}
          stop = False
          rr=0
          while rr < self.n*self.m:
            for job in Sequence:
              index=machines.index(min(machines))
              ma1=copy.deepcopy(machines)
              while job in jobs_list[index]:
                ma1[index]=1000
                index=ma1.index(min(ma1))
              machines[index] = machines[index]+self.p[job][self.M[index]]
              jobs_list[index] = jobs_list[index]+[job]
              mac_list[job].append(self.M[index])
              sequenceMach=jobs_list
              rr+=1
          CM =  {i: 0 for i in self.M}
          CJ =  {j: 0 for j in self.J}
          self.O ={j:{r:mac_list[j][r] for r in range(self.m)} for j in self.J}
          ONum=[len(self.O[j]) for j in self.J]
          pok = False
          for q in range(max(ONum)):
            for v in range(self.n):
              j = Sequence[v]
              if v == 0 and pok == False:
                pok = True
                if (q<len(self.O[j])):
                  i = self.O[j][q]
                  if q == 0:
                    self.S[j][i] = max(self.r[j], self.start,CM[i])
                  else:
                    self.S[j][i] = max(CM[i],CJ[j])
                  self.CC[j][i] = self.S[j][i] + self.p[j][i]
                  iant=i
                  CM[i] = self.CC[j][i]
                CJ[j] = self.CC[j][i]
                jant=j
              else:
                if (q<len(self.O[j])):
                  i = self.O[j][q]
                  if q == 0:
                    self.S[j][i] = max(self.r[j], self.start,CM[i])
                  else:
                    self.S[j][i] = max(CM[i],CJ[j])
                  self.CC[j][i] = self.S[j][i] + self.p[j][i]
                  iant=i
                  CM[i] = self.CC[j][i]
                CJ[j] = self.CC[j][i]
                jant=j
          for j in self.J:
            q = self.O[j][len(self.O[j])-1]
            self.C[j] = self.CC[j][q]
            self.L[j] = self.C[j] - self.d[j]
            self.T[j] = max(0, self.L[j])
            self.E[j] = max(0, -self.L[j])
            if self.T[j]>0: self.U[j] = 1
          results = [{'Job': j,'Machine': self.O[j][i],'Start': self.S[j][self.O[j][i]],'Duration': self.p[j][self.O[j][i]], 'Finish': self.CC[j][self.O[j][i]], 'Due':self.d[j], 'earliness': self.E[j], 'Tardiness': self.T[j]} for j in self.J for i in range(len(self.O[j]))]
          schedule = pd.DataFrame(results)
        if self.ty=="Open-Shop" and optimum==True:
          self.Sumsijk=0
          CM =  {i: 0 for i in self.M}
          CJ =  {j: 0 for j in self.J}
          for i in range(self.m):
            mi=self.M[i]
            ni = len(sequenceMach[i])
            for v in range(ni):
                j = sequenceMach[i][v]
                if v == ni-1:
                  js = sequenceMach[i][0]
                else:
                  js = sequenceMach[i][v+1]
                if v==0:
                  self.S[j][mi] = max(self.r[j],CM[mi],self.start)
                else:
                  self.S[j][mi] = max(self.r[j], CM[mi],CJ[j],self.start)
                self.CC[j][mi] = self.sijk[j][js] + self.S[j][mi] + self.p[j][mi]
                self.C[j]=self.CC[j][mi]
                CM[mi]=self.CC[j][mi]
                CJ[j]=self.CC[j][mi]
                self.L[j] = self.C[j] - self.d[j]
                self.T[j] = max(0, self.L[j])
                self.E[j] = max(0, -self.L[j])
                if self.T[j]>0: self.U[j] = 1
                self.Sumsijk+=self.sijk[j][js]
                j1=j
          results = [{'Job': j,'Machine': self.M[i],'Start': self.S[j][self.M[i]],'Setup' : self.C[j]-self.p[j][self.M[i]]-self.S[j][self.M[i]],'Duration': self.p[j][self.M[i]], 'Finish': self.CC[j][self.M[i]], 'Due': self.d[j],'earliness': self.E[j],'Tardiness': self.T[j]} for i in range(self.m) for j in sequenceMach[i]]
          print("Optimum Solution")
          schedule = pd.DataFrame(results)
        if self.verbose == True:
          print('\nSchedule by Job')
          print(schedule.sort_values(by=['Job','Start']).set_index(['Job', 'Machine']))
          print('\nSchedule by Machine')
          print(schedule.sort_values(by=['Machine','Start']).set_index(['Machine', 'Job']))
        if self.gantt==True:
          self.visualize(results)
        self.compute_objective(self.objective)
        return results

    def showResults(self,Sequence):
        """

        Args:
          Sequence: Sequence of jobs

        """
        self.verbose = True
        results = self.process(Sequence)
        self.verbose = False

        if self.gantt==True:
          self.visualize(results)


    def set_start(self, start):
        """

        Args:
          start: starting time

        """
        self.start = start

    def set_sequence(self,seq):
        """

        Args:
          seq: Sequence of jobs

        Returns:

        """
        Sequence=seq
        self.process(Sequence)
        return Sequence

    def compute_objective(self, objective):
        """

      Args:
        objective: objective function

      Returns: objective function value

      """
        obj=0
        if objective == "AvgC":
          obj=sum(self.C.values())/self.n
          print("AvgC=",obj)
        if objective == "AvgE":
          obj=sum(self.E.values())/self.n
          print("AvgE=",obj)
        if objective == "AvgT":
          obj=sum(self.T.values())/self.n
          print("AvgT=",obj)
        if objective == "MinTotalLateJobs":
          obj=sum(self.U.values())
          print("MinTotalLateJobs=",obj)
        if objective == "WeightedC":
            obj = sum(w * c for w, c in zip(self.w.values(), self.C.values()))
            print("WeightedC=",obj)
        if objective == "WeightedT":
            obj = sum(w * t for w, t in zip(self.w.values(), self.T.values()))
            print("WeightedT=",obj)
        if objective == "WeightedE":
            obj = sum(w * e for w, e in zip(self.w.values(), self.E.values()))
            print("WeightedE=",obj)
        if objective == "WeightedT+E":
            obj = sum(
                w2 * t for w2, t in zip(self.w2.values(), self.T.values())
            ) + sum(w1 * e for w1, e in zip(self.w1.values(), self.E.values()))
            print("WeightedT+E=",obj)
        if objective == "Tmax":
          obj=max(self.T.values())
          print("Tmax=",obj)
        if objective == "Emax":
          obj=max(self.E.values())
          print("Emax=",obj)
        if objective == "Cmax":
          obj=max(self.C.values())
          print("Cmax=",obj)
        if objective == "Lmax":
          obj=max(self.L.values())
          print("Lmax=",obj)
        if objective is None:
          obj=[]
          obj.append(sum(self.C.values())/self.n)
          print("AvgC=",obj)
          obj.append(sum(self.E.values())/self.n)
          print("AvgE=",obj)
          obj.append(sum(self.T.values())/self.n)
          print("AvgT=",obj)
        return obj

    def FCFS(self):
        """
        FCFS (First Come First Serve) rule to schedule jobs.
        Returns: Sequence of jobs to be scheduled

        """
        Sequence = self.J
        self.process(Sequence)
        return Sequence

    def RANDOM(self):
        """
        RANDOM (Random) rule to schedule jobs.
        Returns: Sequence of jobs to be scheduled

        """
        Sequence = random.sample(self.J,k=self.n)
        self.process(Sequence)
        return Sequence

    def LCFS(self):
        """
        LCFS (Last Come First) rule to schedule jobs.
        Returns: Sequence of jobs to be scheduled

        """
        Sequence = self.J[::-1]
        self.process(Sequence)
        return Sequence

    FIFO = FCFS
    LIFO = LCFS

    def SPT(self):
        """
        SPT (Shortest Processing Time) rule to schedule jobs.
        Returns: Sequence of jobs to be scheduled

        """
        if self.preced:
          Sequence=[]
          b = True
          G2=self.G.copy()
          while b:
            F=[]
            for i in G2:
              if list(G2.predecessors(i))==[]:
                F.append(i)
            p1={j:sum(self.p[j].values()) for j in F}
            P1=SingleMachineSP(len(F),F,p1)
            s=P1.SPT()
            G2.remove_nodes_from(F)
            if G2.number_of_nodes()==0:
              b=False
            Sequence=Sequence+s
        else:
          Sequence = [x for _, x in sorted(zip(zip(self.r.values(),[sum(self.p[j].values()) for j in self.J]), self.J))]
        self.process(Sequence)
        return Sequence

    def LPT(self):
        """
        LPT (Longest Processing Time) rule to schedule jobs.
        Returns: Sequence of jobs to be scheduled

        """
        if self.preced:
          Sequence=[]
          b = True
          G2=self.G.copy()
          while b:
            F=[]
            for i in G2:
              if list(G2.predecessors(i))==[]:
                F.append(i)
            p1={j:sum(self.p[j].values()) for j in F}
            print(p1)
            P1=SingleMachineSP(len(F),F,p1)
            s=P1.LPT()
            G2.remove_nodes_from(F)
            if G2.number_of_nodes()==0:
              b=False
            Sequence=Sequence+s
        else:
          Sequence = [x for _, x in sorted(zip(zip(self.r.values(),[-sum(self.p[j].values()) for j in self.J]), self.J))]
        self.process(Sequence)
        return Sequence

    def WSPT(self):
        """
        WSPT (Weighted Shortest Processing Time) rule to schedule jobs.
        Returns: Sequence of jobs to be scheduled

        """
        rs = [x/y for x, y in zip([sum(self.p[j].values()) for j in self.J], self.w.values())]
        Sequence = [x for _, x in sorted(zip(zip(self.r.values(), rs), self.J))]
        self.process(Sequence)
        return Sequence

    def EDD(self):
        """
        EDD (Earliest Due Date) rule to schedule jobs.
        Returns: Sequence of jobs to be scheduled

        """
        Sequence = [x for _, x in sorted(zip(zip(self.r.values(),self.d.values()), self.J))]
        self.process(Sequence)
        return Sequence

    def LDD(self):
        """
        LDD (Latest Due Date) rule to schedule jobs.
        Returns: Sequence of jobs to be scheduled

        """
        Sequence = [x for _, x in sorted(zip(zip(self.r.values(),[-k for k in self.d.values()]), self.J))]
        self.process(Sequence)
        return Sequence

    def O2opt(self):
        T1 = 0
        T2 = 0
        a = {j:self.p[j][self.M[0]] for j in self.J}
        b = {j:self.p[j][self.M[1]] for j in self.J}
        a[0]=0
        b[0]=0
        l = 0
        r = 0
        S = []
        for j in self.J:
          T1 = T1 + a[j]
          T2 = T2 + b[j]
          if a[j]>=b[j]:
            if a[j]>=b[r]:
              S = S + [r]
              r = j
            else:
              S = S + [j]
          else:
            if b[j]>=a[l]:
              S = [l] + S
              l = j
            else:
              S = [j] + S
          print(S,r,l)
        if T1-a[l]<T2-b[r]:
          S1 = S + [r] + [l]
          S2 = [l] + S +[r]
        else:
          S1 = [l] + S + [r]
          S2 = [r] + [l] + S
        while (0 in S1): S1.remove(0)
        while (0 in S2): S2.remove(0)
        sequenceMach=[S1,S2]
        self.process([],sequenceMach,True)
        return sequenceMach


    def Johnson(self, data: dict):
        """Function that takes a dictionary with the jobs, machines and the processing time snd return the sequence of jobs using the johnson algorithm

        Steps
        ❑ Step 1. Schedule the group of jobs U that are shorter on the
        first machine than the second.
        U = { j | p1j < p2j }
        ❑ Step 2. Schedule the group of jobs V that are shorter on the
        second machine than the first.
        V = { j | p1j  p2j }
        ❑ Step 3. Arrange jobs in U in non-decreasing order by their
        processing times on the first machine.
        ❑ Step 4. Arrange jobs in V in non-increasing order by their
        processing times on the second machine.
        ❑ Step 5. Concatenate U and V and that is the processing order
        for both machines.
        **The ties are broken at random.

        Args:
            data: dictionary with the jobs, machines and the processing time
        Returns:
            sequence of jobs
        """
        # Step 1
        U = []
        for i in data:
            if data[i][self.M[0]] < data[i][self.M[1]]:
                U.append(i)
        # Step 2
        V = []
        for i in data:
            if data[i][self.M[0]] >= data[i][self.M[1]]:
                V.append(i)
        # Step 3
        U = sorted(U, key=lambda x: data[x][self.M[0]])
        # Step 4
        V = sorted(V, key=lambda x: data[x][self.M[1]], reverse=True)
        # Step 5
        Sequence=U+V
        self.process(Sequence)
        return Sequence

    def CDS(self, data: dict):
        """Function that takes a dictionary with the jobs, machines and the processing time and return the sequence of jobs using the johnson algorithm
        Steps
        ❑ Step 1. Schedule the group of jobs U that are shorter on the
        first machine than the second.
        U = { j | p1j < p2j }
        ❑ Step 2. Schedule the group of jobs V that are shorter on the
        second machine than the first.
        V = { j | p1j >= p2j }
        ❑ Step 3. Arrange jobs in U in non-decreasing order by their
        processing times on the first machine.
        ❑ Step 4. Arrange jobs in V in non-increasing order by their
        processing times on the second machine.
        ❑ Step 5. Concatenate U and V and that is the processing order
        for both machines.
        **The ties are broken at random.

        Args:
            data: dictionary with the jobs, machines and the processing time
        Returns:
            sequence of jobs
        """
        p1=np.array([[self.p[j][i] for i in self.M] for j in self.J])
        if self.m==3:
            if min(np.array(p1.T[0])) >= max(np.array(p1.T[1])) or min(np.array(p1.T[2])) >= max(np.array(p1.T[1])):
              print("CDS get the optimal schedule for the minimum makespan")
            G = {
                j: {
                    0: self.p[j][self.M[0]] + self.p[j][self.M[1]],
                    1: self.p[j][self.M[1]] + self.p[j][self.M[2]],
                }
                for j in self.J
            }
            # Step 1
            U = []
            for i, value in G.items():
                if value[0] < G[i][1]:
                    U.append(i)
            # Step 2
            V = []
            for i, value_ in G.items():
                if value_[0] >= G[i][1]:
                    V.append(i)
            # Step 3
            U = sorted(U, key=lambda x: G[x][0])
            # Step 4
            V = sorted(V, key=lambda x: G[x][1], reverse=True)
            # Step 5
            Sequence=U+V
            Sequence=U+V
            self.process(Sequence)
            return Sequence

        else:
            J0=[]
            for k in range(self.m):
                G = {
                    self.J[i]: {0: sum(p1[i][: k + 1]), 1: sum(p1[i][k + 1 :])}
                    for i in range(self.n)
                }
                print("Groups",G)
                # Step 1
                U = []
                for i, value__ in G.items():
                    if value__[0] < G[i][1]:
                        U.append(i)
                # Step 2
                V = []
                for i, value___ in G.items():
                    if value___[0] >= G[i][1]:
                        V.append(i)
                # Step 3
                U = sorted(U, key=lambda x: G[x][0])
                # Step 4
                V = sorted(V, key=lambda x: G[x][1], reverse=True)
                # Step 5
                Sequence=U+V
                self.process(Sequence)
                J0.append(Sequence)
            print(J0)
            return J0

    def twoOpt(self,s):
        sol=s
        j = random.randint(0,len(sol)-1)
        k=random.randint(0,len(sol)-1)
        while (k==j):
          k=random.randint(0,len(sol)-1)
        a=sol[k]
        b=sol[j]
        sol[j]=a
        sol[k]=b
        return sol

    def decreaseT(self,t,decreaseMethod,alpha):
        if decreaseMethod=='Geometric':
          return alpha*t
        if decreaseMethod=='Lineal':
          return t-alpha

    def SA(self,s,MaxIter,TemIni,decreaseMethod='Geometric',alpha=0.98):
        """

        Args:
          s: initial solution
          MaxIter: maximum number of iterations
          TemIni: initial temperature
          decreaseMethod: method to decrease temperature
          alpha: parameter to decrease temperature

        Returns:

        """
        Best=s
        self.process(s)
        c1=self.compute_objective(self.objective)
        cb=self.compute_objective(self.objective)
        k=0
        t=TemIni
        Val=[[k,c1,cb,0,(t/1000),s,Best]]
        while (k<MaxIter):
            k += 1
            R=self.twoOpt(s)
            self.process(R)
            c2=self.compute_objective(self.objective)
            p=random.random()
            prob=[p,np.exp(-(c2-c1)/t)]
            if c2<c1 or p<np.exp(-(c2-c1)/t):
              s=R
              self.process(s)
              c1=self.compute_objective(self.objective)
            t=self.decreaseT(t,decreaseMethod,alpha);
            if c1<cb:
              Best=s.copy()
              self.process(Best)
              cb=self.compute_objective(self.objective)
            Val1=[k,c1,cb,prob[0],(t/1000),s,Best]
            Val.append(Val1)
        df=pd.DataFrame(Val)
        df
        x=df[0]
        y=df[1]
        plt.plot(x, y,linestyle='-')
        return Best

    def optimizationModel(self,problemName,objectiveFunction):
        """

        Args:
          problemName: name of the problem
          objectiveFunction: objective function

        Returns: optimization model
        """
        self.objectiveFunction=objectiveFunction
        # Problem Definition
        self.problemSP=LpProblem(problemName,LpMinimize)
        #Decision Variables
        self.x=LpVariable.dicts('x',((j,i) for j in self.J for i in self.M),lowBound=0,cat='Continuous')
        self.c = LpVariable.dicts('c', iter(self.J), lowBound=0, cat='Continuous')
        self.E = LpVariable.dicts('E', iter(self.J), lowBound=0, cat='Continuous')
        self.T = LpVariable.dicts('T', iter(self.J), lowBound=0, cat='Continuous')
        self.U = LpVariable.dicts('U', iter(self.J), lowBound=0, cat='Binary')
        self.cmax=LpVariable('cmax',cat='Continuous')
        self.Tmax=LpVariable('Tmax',cat='Continuous')
        self.Emax=LpVariable('Emax',cat='Continuous')
        self.y=LpVariable.dicts('y',((u,v,i) for u in self.J for v in self.J for i in self.M),cat='Binary')
        # Objective functions
        self.f0=LpAffineExpression(self.cmax)
        self.f1=LpAffineExpression(lpSum(self.c[j] for j in self.J)/self.n)
        self.f2=LpAffineExpression(lpSum(self.E[j] for j in self.J)/self.n)
        self.f3=LpAffineExpression(lpSum(self.T[j] for j in self.J)/self.n)
        self.f4=LpAffineExpression(lpSum(self.U[j] for j in self.J))
        self.f5=LpAffineExpression(lpSum(self.w[j]*self.c[j] for j in self.J))
        self.f6=LpAffineExpression(lpSum(self.w[j]*self.T[j] for j in self.J))
        self.f7=LpAffineExpression(lpSum(self.w[j]*self.E[j] for j in self.J))
        self.f8=LpAffineExpression(lpSum((self.w1[j]*self.E[j]+self.w2[j]*self.T[j]) for j in self.J))
        self.f9=LpAffineExpression(self.Tmax)
        self.f10=LpAffineExpression(self.Emax)
        if objectiveFunction =="Cmax":
          self.problemSP.setObjective(self.f0)
        if objectiveFunction == "AvgC":
          self.problemSP.setObjective(self.f1)
        if objectiveFunction == "AvgE":
          self.problemSP.setObjective(self.f2)
        if objectiveFunction == "AvgT":
          self.problemSP.setObjective(self.f3)
        if objectiveFunction == "MinTotalLateJobs":
          self.problemSP.setObjective(self.f4)
        if objectiveFunction == "WeightedC":
          self.problemSP.setObjective(self.f5)
        if objectiveFunction == "WeightedT":
          self.problemSP.setObjective(self.f6)
        if objectiveFunction == "WeightedE":
          self.problemSP.setObjective(self.f7)
        if objectiveFunction == "WeightedT+E":
          self.problemSP.setObjective(self.f8)
        if objectiveFunction == "Tmax":
          self.problemSP.setObjective(self.f9)
        if objectiveFunction == "Emax":
          self.problemSP.setObjective(self.f10)
        if objectiveFunction is None:
            print("No objective defined, the makespan will be minimized")
            self.problemSP.setObjective(self.f0)
        #Sequence constraints
        if self.ty!="Open-Shop":
          for j in self.J:
              for h in range(len(self.O[j])-1):
                  h0=self.O[j][h]
                  h1=self.O[j][h+1]
                  self.problemSP += (
                      self.x[j, h0] + self.p[j][h0] <= self.x[j, h1],
                      f"Seq{str(j)}{str(h)}",
                  )
                  if h == 0:
                      self.problemSP += (self.x[j,h0]>=self.r[j], f"Start{str(j)}{str(h)}")
        # Ending constraints
        if self.ty!="Open-Shop":
          for j in self.J:
            h=len(self.O[j])-1
            hf=self.O[j][h]
            self.problemSP+=self.x[j,hf]+self.p[j][hf]==self.c[j],'End'+j
        else:
          for j in self.J:
            for i in self.M:
              self.problemSP+=self.x[j,i]+self.p[j][i]<=self.c[j],f'End{str(j)}{str(i)}'
          
        #earliness and tardiness constraints
        MM=10000000
        for j in self.J:
          self.problemSP+=self.c[j]==self.d[j]+self.T[j]-self.E[j],'EYT'+j
          self.problemSP+=self.T[j]<=self.U[j]*MM,'U'+j
          self.problemSP+=self.E[j]<=self.Emax
          self.problemSP+=self.T[j]<=self.Tmax
        #non-interference constraints
        for i in self.M:
          for u in self.J:
            for v in self.J:
              if (u!=v):
                self.problemSP+=self.x[v,i]-self.x[u,i]+MM*(1-self.y[u,v,i])>=self.p[u][i]
                self.problemSP+=self.x[u,i]-self.x[v,i]+MM*(self.y[u,v,i])>=self.p[v][i]
        # makespan constraints
        for j in self.J:
          #h=self.O[j][len(self.O[j])-1]
          #self.problemSP+=self.x[j,h]+self.p[j][h]<=self.cmax
          self.problemSP+=self.c[j]<=self.cmax
        # Precedence-constraints
        if self.preced==True:
          for (u,v) in self.prec:
            for i in self.M:
              self.problemSP+=self.y[u,v,i]==1

    def showModel(self,filename):
          """

          Args: name of file to write the model

          Returns: None

          """
          self.problemSP.writeLP(filename)

    def solve(self):
          """
          solve the optimization problem
          Returns: array with the solution

          """
          self.problemSP.solve()
          print ("Status: ",LpStatus[self.problemSP.status])
          print("Objective Function (",self.objectiveFunction,") = ",self.problemSP.objective.value())
          results = [{'Job': j,'Machine': self.O[j][i],'Start': value(self.x[j,self.O[j][i]]),'Duration': self.p[j][self.O[j][i]], 'Finish': value(self.x[j,self.O[j][i]]+self.p[j][self.O[j][i]]), 'Due': self.d[j],  'earliness': value(self.E[j]),'Tardiness': value(self.T[j])} for j in self.J for i in self.O[j]]
          schedule = pd.DataFrame(results)
          print('\nSchedule by Job')
          print(schedule.sort_values(by=['Job','Start']).set_index(['Job', 'Machine']))
          print('\nSchedule by Machine')
          print(schedule.sort_values(by=['Machine','Start']).set_index(['Machine', 'Job']))
          return results


    def optimizationModelOS(self,problemName,objectiveFunction):
        """
        Optimization model for scheduling.

        Args:
          problemName: name of the problem
          objectiveFunction: objective function

        """
        self.objectiveFunction=objectiveFunction
        # Problem Definition
        self.problemSP=LpProblem(problemName,LpMinimize)
        #Decision Variables
        self.x=LpVariable.dicts('x',((g,h,j) for g in self.M for h in self.M for j in self.J),lowBound=0,upBound=1,cat='Binary')
        self.y=LpVariable.dicts('y',((u,v,i) for u in self.J for v in self.J for i in self.M),lowBound=0,upBound=1,cat='Binary')
        self.s = LpVariable.dicts('s', ((j,i) for j in self.J for i in self.M), lowBound=0, cat='Continuous')
        self.c = LpVariable.dicts('c', iter(self.J), lowBound=0, cat='Continuous')
        self.E = LpVariable.dicts('E', iter(self.J), lowBound=0, cat='Continuous')
        self.T = LpVariable.dicts('T', iter(self.J), lowBound=0, cat='Continuous')
        self.U = LpVariable.dicts('U', iter(self.J), lowBound=0, cat='Binary')
        self.cmax=LpVariable('cmax',cat='Continuous')
        self.Tmax=LpVariable('Tmax',cat='Continuous')
        self.Emax=LpVariable('Emax',cat='Continuous')
        # Objective function
        self.f0=LpAffineExpression(self.cmax)
        self.f1=LpAffineExpression(lpSum(self.c[j] for j in self.J)/self.n)
        self.f2=LpAffineExpression(lpSum(self.E[j] for j in self.J)/self.n)
        self.f3=LpAffineExpression(lpSum(self.T[j] for j in self.J)/self.n)
        self.f4=LpAffineExpression(lpSum(self.U[j] for j in self.J))
        self.f5=LpAffineExpression(lpSum(self.w[j]*self.c[j] for j in self.J))
        self.f6=LpAffineExpression(lpSum(self.w[j]*self.T[j] for j in self.J))
        self.f7=LpAffineExpression(lpSum(self.w[j]*self.E[j] for j in self.J))
        self.f8=LpAffineExpression(lpSum((self.w1[j]*self.E[j]+self.w2[j]*self.T[j]) for j in self.J))
        self.f9=LpAffineExpression(self.Tmax)
        self.f10=LpAffineExpression(self.Emax)
        if objectiveFunction =="Cmax":
          self.problemSP.setObjective(self.f0)
        if objectiveFunction == "AvgC":
          self.problemSP.setObjective(self.f1)
        if objectiveFunction == "AvgE":
          self.problemSP.setObjective(self.f2)
        if objectiveFunction == "AvgT":
          self.problemSP.setObjective(self.f3)
        if objectiveFunction == "MinTotalLateJobs":
          self.problemSP.setObjective(self.f4)
        if objectiveFunction == "WeightedC":
          self.problemSP.setObjective(self.f5)
        if objectiveFunction == "WeightedT":
          self.problemSP.setObjective(self.f6)
        if objectiveFunction == "WeightedE":
          self.problemSP.setObjective(self.f7)
        if objectiveFunction == "WeightedT+E":
          self.problemSP.setObjective(self.f8)
        if objectiveFunction == "Tmax":
          self.problemSP.setObjective(self.f9)
        if objectiveFunction == "Emax":
          self.problemSP.setObjective(self.f10)
        if objectiveFunction is None:
            print("No objective defined, the makespan will be minimized")
            self.problemSP.setObjective(self.f0)
        MM=10000000      
        # Allocation constraints
        #earliness and tardiness constraints
        for j in self.J:
          for i in self.M:
            self.problemSP+=self.c[j]>=self.s[j,i]+self.p[j][i]
          self.problemSP+=self.c[j]==self.d[j]+self.T[j]-self.E[j],'EYT'+j
          self.problemSP+=self.T[j]<=self.U[j]*MM,'U'+j
          self.problemSP+=self.E[j]<=self.Emax
          self.problemSP+=self.T[j]<=self.Tmax
          self.problemSP+=self.c[j]<=self.cmax
        for i in self.M:
          for v in self.J:
            for q in self.J:
              if (v!=q):
                self.problemSP+=self.s[v,i]+self.p[v][i]<=self.s[q,i]+MM*(1-self.y[v,q,i])
        for j in self.J:
          for g in self.M:
            for h in self.M:
              if (g!=h):
                self.problemSP+=self.s[j,g]+self.p[j][g]<=self.s[j,h]+MM*(1-self.x[g,h,j])

        for i in self.M:
          for v in self.J:
            for q in self.J:
              if (v!=q):
                self.problemSP+=self.y[v,q,i]+self.y[q,v,i]==1
        for j in self.J:
          for g in self.M:
            for h in self.M:
              if (g!=h):
                self.problemSP+=self.x[g,h,j]+self.x[h,g,j]==1
        # precedence constraints
        if self.preced==True:
          for (v,q) in self.prec:
            self.problemSP+=self.s[q]>=self.c[v]

    def solveOS(self):
        """
          Solve the optimization problem version 2.

          Returns: array of results.

          """
        self.problemSP.solve()
        for j in self.J:
          print(j,value(self.c[j]))
          
        print ("Status: ",LpStatus[self.problemSP.status])
        results = [{'Job': j,'Machine': i,'Start': value(self.s[j,i]),'Duration': self.p[j][i], 'Finish': value(self.s[j,i])+self.p[j][i], 'Due': self.d[j],'earliness': value(self.E[j]),'Tardiness': value(self.T[j])} for i in self.M for j in self.J ]
        print("Objective Function (",self.objectiveFunction,") = ",self.problemSP.objective.value())
        schedule = pd.DataFrame(results)
        print('\nSchedule by Job')
        print(schedule.sort_values(by=['Job','Start']).set_index(['Job', 'Machine']))
        print('\nSchedule by Machine')
        print(schedule.sort_values(by=['Machine','Start']).set_index(['Machine', 'Job']))
        return results




class ParallelMachineSP:
    """
    ParallelMachineSP (Parallel Machine Scheduling Problem) class: this class implements the Parallel Machine Scheduling Problem. We define a simple problem like P||gamma. We implement dispatching rules and some algorithms to solve specific problems. This class supports Uniform machines. We developed specific functions to describe the solution, compute the Objective function(gamma) and plot the gantt chart.

    Attributes:
    Mandatory attributes:
      n: number of jobs
      J: list of jobs
      p: processing times for each job
      m: number of machines
      M: list of machines
      ty: type of scheduling problem
    Optional attributes:
      prec: precedence
      preced: if True, precedences is active, False otherwise
      G: graph of precedences
      d: due date for each job
      r: start date for each job
      w: weight for each job
      w1: weight of late for each job
      w2: weight of early for each job
      sijk: setup time for each job and machine
      start: start time for the scheduling problem
      objective: objective function
      gantt: if True, visualize the scheduling problem
      verbose: if True, print the scheduling problem
    Variables and computations:
      S: start time for job j
      C: completion time for job j
      L: lateness for job j
      T: tardiness for job j
      E: earliness for job j
      U: unit penalty of job j or Late job
      Tmax: maximum tardiness
      Emax: maximum earliness
      Cmax: maximum completion time (makespan)
      Sumsijk: sum of setup times for each job and machine
    Variables for the optimization problem:
      objectiveFunction: objective function
      problemSP: name of the scheduling problem
      x:
      c:
      cmax:
      f0:
      f1:
      f2:
      f3:
      f4:
      f5:
      f6:
      f7:
      f8:
      f9:
      f10:
    """

    def __init__(self, n ,J , m, M, p, ty, prec = {}, v= {}, d = {}, r ={},w = {}, w1 = {}, w2 = {}, sijk = {}, start = 0, objective = 0, gantt = False, verbose = False):
        """

        Args:
        Mandatory attributes:
          n: number of jobs
          J: list of jobs
          p: processing times for each job
          m: number of machines
          M: list of machines
          ty: type of scheduling problem
        Optional attributes:
          prec: precedence
          preced: if True, precedences is active, False otherwise
          G: graph of precedences
          d: due date for each job
          r: start date for each job
          w: weight for each job
          w1: weight of late for each job
          w2: weight of early for each job
          sijk: setup time for each job and machine
          start: start time for the scheduling problem
          objective: objective function
          gantt: if True, visualize the scheduling problem
          verbose: if True, print the scheduling problem  n:

        """
        self.n = n
        self.J = J
        self.p = p
        self.m = m
        self.M = M
        self.ty=ty
        if prec == {}:
          self.prec = {j:0 for j in self.J}
          self.preced=False
        else:
          self.prec=prec
          self.G = nx.DiGraph(list(self.prec))
          if (set(self.J-self.G.nodes()))!=[]:
            for j in (set(self.J-self.G.nodes())):
              self.G.add_node(j)          
          self.preced=True
        if v == {}:
          self.v= {i:{j:1 for j in self.J} for i in self.M}
        else:  
          if self.ty == "Q":
            self.v= {i:{j:v[i] for j in self.J} for i in self.M}
          if self.ty=="R":
            self.v= v
          if self.ty=="P":
            self.v= {i:{j:1 for j in self.J} for i in self.M}
        self.d = {j:0 for j in self.J} if d == {} else d
        self.r = {j:0 for j in self.J} if r == {} else r
        self.w = {j:1 for j in self.J} if w == {} else w
        self.w1 = {j:1 for j in self.J} if w1 == {} else w1
        self.w2 = {j:1 for j in self.J} if w2 == {} else w2
        self.sijk = {i:{j:0 for j in self.J} for i in self.J} if sijk == {} else sijk
        self.start = start
        self.objective=objective
        self.gantt = gantt
        self.verbose = verbose
        self.S =  {j: 0 for j in self.J}
        self.C =  {j: 0 for j in self.J}
        self.L =  {j: 0 for j in self.J}
        self.T =  {j: 0 for j in self.J}
        self.E =  {j: 0 for j in self.J}
        self.U =  {j: 0 for j in self.J}
        self.Tmax=0
        self.Emax=0
        self.Cmax=0
        self.Sumsijk=0

    def MSPT(self,sequence):
        """
      M
      Args:
        sequence: sequence of jobs

      Returns: sequence of jobs for each machine

      """
        machines = [0 for _ in range(self.m)]
        jobs_list = [[] for _ in range(self.m)]
        for job in sequence:
          index=machines.index(min(machines))
          machines[index] = machines[index]+self.p[job]
          jobs_list[index] = jobs_list[index]+[job]
          sequenceMach=jobs_list
        print(sequenceMach)
        print("Cmax ",max(machines))
        self.process(sequenceMach)
        return sequenceMach

    def visualize_Graph(self,results):
      """
        Create a chart to see a graph with precedence relations and the solution.
        Args:
          results:  is an array with the results of the schedule generation or
          optimization model

        Returns: the gantt chart

        """
      self.G= nx.DiGraph(list(self.prec))
      schedule = pd.DataFrame(results)
      JOBS = sorted(list(schedule['Job'].unique()))
      MACHINES = sorted(list(schedule['Machine'].unique()))
      MA=list(schedule['Machine'])
      JO=list(schedule['Job'])
      MA={JO[j]:self.M.index(MA[j])+1 for j in range(self.n)}
      for layer, nodes in enumerate(nx.topological_generations(self.G)):
          for node in nodes:
              self.G.nodes[node]["layer"] = layer
      ColorLegend = {MACHINES[i]: i+1 for i in range(self.m)}
      values = [MA.get(node, 0) for node in self.G.nodes()]
      jet = cm = plt.get_cmap('jet')
      cNorm  = colors.Normalize(vmin=0, vmax=max(values))
      scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
      pos = nx.multipartite_layout(self.G, subset_key="layer")
      fig = plt.figure(1)
      ax = fig.add_subplot(1,1,1)
      for label in ColorLegend:
        ax.plot([0],[0],color=scalarMap.to_rgba(ColorLegend[label]),label=label)
      nx.draw_networkx(self.G,pos, cmap = jet, vmin=0, vmax= max(values),node_color=values,with_labels=True,ax=ax)
      ax.set_title("Graph of precedences")
      plt.axis('off')
      fig.set_facecolor('w')
      plt.legend()
      fig.tight_layout()
      return plt.show()

    def visualize(self,results):
        """
        Create a gantt chart.
        Args:
          results:  is an array with the results of the schedule generation or
          optimization model

        Returns: the gantt chart

        """
        schedule = pd.DataFrame(results)
        JOBS = sorted(list(schedule['Job'].unique()))
        MACHINES = sorted(list(schedule['Machine'].unique()))
        makespan = schedule['Finish'].max()
        bar_style = {'alpha':1.0, 'lw':25, 'solid_capstyle':'butt'}
        text_style = {'color':'white', 'weight':'bold', 'ha':'center', 'va':'center'}
        colors = plt.cm.tab20.colors
        schedule.sort_values(by=['Job', 'Start'])
        schedule.set_index(['Job', 'Machine'], inplace=True)
        fig, ax = plt.subplots(2,1, figsize=(12, 5+(len(JOBS)+len(MACHINES))/4))
        for jdx, j in enumerate(JOBS, 1):
            for mdx, m in enumerate(MACHINES, 1):
                if (j,m) in schedule.index:
                    xs = schedule.loc[(j,m), 'Start']
                    xf = schedule.loc[(j,m), 'Finish']
                    ax[0].plot([xs, xf], [jdx]*2, c=colors[(mdx)%len(colors)], **bar_style)
                    ax[0].text((xs + xf)/2, jdx, m, **text_style)
                    ax[1].plot([xs, xf], [mdx]*2, c=colors[(jdx)%len(colors)], **bar_style)
                    ax[1].text((xs + xf)/2, mdx, j, **text_style)
        ax[0].set_title('Job Schedule')
        ax[0].set_ylabel('Job')
        ax[1].set_title('Machine Schedule')
        ax[1].set_ylabel('Machine')
        for idx, s in enumerate([JOBS, MACHINES]):
            ax[idx].set_ylim(0.5, len(s) + 0.5)
            ax[idx].set_yticks(range(1, 1 + len(s)))
            ax[idx].set_yticklabels(s)
            #ax[idx].text(makespan, ax[idx].get_ylim()[0]-0.2, "{0:0.1f}".format(makespan), ha='center', va='top')
            ax[idx].plot([makespan]*2, ax[idx].get_ylim(), 'r--')
            ax[idx].set_xlabel('Time')
            ax[idx].grid(True)
        fig.tight_layout()
        red_patch = mpatches.Patch(color='red',fill='',linestyle='--', label=f"Cmax = {makespan}")
        fig.legend(handles=[red_patch],loc='lower right')
        return plt.show()

    def process(self,sequence,sequenceMach={}):
        """

        Args:
          Sequence: Sequence of jobs
          sequenceMach: Sequence of machines for each job
          optimum: if True, compute optimum solution

        Returns: results (array  with the computations of the schedule)

        """
        if sequenceMach=={}:
            machines = [0 for _ in range(self.m)]
            jobs_list = [[] for _ in range(self.m)]
            for job in sequence:
              index=machines.index(min(machines))
              machines[index] = machines[index]+self.p[job]/self.v[self.M[index]][job]
              jobs_list[index] = jobs_list[index]+[job]
              sequenceMach=jobs_list
        self.Sumsijk=0
        for i in range(self.m):
            ni = len(sequenceMach[i])
            for q in range(ni):
                j = sequenceMach[i][q]
                js = sequenceMach[i][0] if q == ni-1 else sequenceMach[i][q+1]
                if q==0:
                  self.S[j] = max(self.r[j],self.start)
                else:
                  self.S[j] = max(self.r[j], self.C[j1],self.start)
                self.C[j] = self.sijk[j][js] + self.S[j] + self.p[j]/self.v[self.M[i]][j]
                self.L[j] = self.C[j] - self.d[j]
                self.T[j] = max(0, self.L[j])
                self.E[j] = max(0, -self.L[j])
                if self.T[j]>0: self.U[j] = 1
                self.Sumsijk+=self.sijk[j][js]
                j1=j
        if self.preced==True:
          machines=[0 for i in range(self.m)]
          jobs_list=[[] for i in range(self.m)]
          mac_list={j:[] for j in self.J}
          for job in sequence:
            index=machines.index(min(machines))
            machines[index] = machines[index]+self.p[job]/self.v[self.M[index]][job]
            jobs_list[index] = jobs_list[index]+[job]
            sequenceMach=jobs_list
            mac_list[job].append(index)
          CC =  {j:[0 for i in range(self.m)]  for j in self.J}
          CM =  {i: 0 for i in range(self.m)}
          CJ =  {j: 0 for j in self.J}
          G1 = self.G.copy()
          for v in range(self.n):
            j = sequence[v]
            i = mac_list[j][0]
            if v==0:
              self.S[j] = max(self.r[j],self.start)
            else:
              ja=0
              for q in list(G1.predecessors(j)): ja=max(ja,CJ[q])
              self.S[j] = max(0,CM[i],ja)
            CC[j][i] = self.S[j] + self.p[j]/self.v[self.M[i]][j]
            CM[i]=CC[j][i]
            CJ[j]=CC[j][i]
            self.C[j]=CC[j][i]
            self.L[j] = self.C[j] - self.d[j]
            self.T[j] = max(0, self.L[j])
            self.E[j] = max(0, -self.L[j])
            if self.T[j]>0: self.U[j] = 1
            j1=j
        results = [{'Job': j,'Machine': self.M[i],'Start': self.S[j],'Setup' : self.C[j]-self.p[j]/self.v[self.M[i]][j]-self.S[j],'Duration': self.p[j]/self.v[self.M[i]][j], 'Finish': self.C[j], 'Due': self.d[j],'earliness': self.E[j],'Tardiness': self.T[j]} for i in range(self.m) for j in sequenceMach[i]]
        schedule = pd.DataFrame(results)
        if self.verbose == True:
          print('\nSchedule by Job')
          print(schedule.sort_values(by=['Job','Start']).set_index(['Job', 'Machine']))
          print('\nSchedule by Machine')
          print(schedule.sort_values(by=['Machine','Start']).set_index(['Machine', 'Job']))
        if self.gantt==True:
          self.visualize(results)
        self.compute_objective(self.objective)
        return results

    def showResults(self,sequenceMach):
        """

        Args:
          sequenceMach: Sequence of machines for each job

        Returns: results (array  with the computations of the schedule)
        """
        self.verbose=True
        results = self.process(sequenceMach)
        if self.gantt==True:
          self.visualize(results)
        self.verbose=False

    def set_start(self, start):
        """

        Args:
          start: start time

        """
        self.start = start

    def set_sequence(self,seq):
        """

        Args:
          seq: sequence of jobs

        """
        Sequence=seq
        self.process(Sequence)
        return Sequence

    def compute_objective(self, objective):
        """

      Args:
        objective: objective function

      Returns: objective function value

      """

        obj=0
        if objective == "AvgC":
          obj=sum(self.C.values())/self.n
          print("AvgC=",obj)
        if objective == "AvgE":
          obj=sum(self.E.values())/self.n
          print("AvgE=",obj)
        if objective == "AvgT":
          obj=sum(self.T.values())/self.n
          print("AvgT=",obj)
        if objective == "MinTotalLateJobs":
          obj=sum(self.U.values())
          print("MinTotalLateJobs=",obj)
        if objective == "WeightedC":
            obj = sum(w * c for w, c in zip(self.w.values(), self.C.values()))
            print("WeightedC=",obj)
        if objective == "WeightedT":
            obj = sum(w * t for w, t in zip(self.w.values(), self.T.values()))
            print("WeightedT=",obj)
        if objective == "WeightedE":
            obj = sum(w * e for w, e in zip(self.w.values(), self.E.values()))
            print("WeightedE=",obj)
        if objective == "WeightedT+E":
            obj = sum(
                w * t for w, t in zip(self.w2.values(), self.T.values())
            ) + sum(w * e for w, e in zip(self.w1.values(), self.E.values()))
            print("WeightedT+E=",obj)
        if objective == "Tmax":
          obj=max(self.T.values())
          print("Tmax=",obj)
        if objective == "Emax":
          obj=max(self.E.values())
          print("Emax=",obj)
        if objective == "Cmax":
          obj=max(self.C.values())
          print("Cmax=",obj)
        if objective == "Lmax":
          obj=max(self.L.values())
          print("Lmax=",obj)
        if objective == "sijk":
          obj=self.Sumsijk
          print("Sum of sijk=",obj)
        if objective is None:
          obj=[]
          obj.append(sum(self.C.values())/self.n)
          print("AvgC=",obj)
          obj.append(sum(self.E.values())/self.n)
          print("AvgE=",obj)
          obj.append(sum(self.T.values())/self.n)
          print("AvgT=",obj)
        return obj

    def FCFS(self):
      """
      FCFS (First Come First Served) rule for scheduling.

      Returns: Sequence of jobs

      """
      Sequence = self.J
      self.process(Sequence)
      return Sequence

    def RANDOM(self):
        """
        RANDOM rule for scheduling.

        Returns: Sequence of jobs

        """
        Sequence = random.sample(self.J,k=self.n)
        self.process(Sequence)
        return Sequence

    def LCFS(self):
        """
        LCFS (Last Come First Served) rule for scheduling.

        Returns: Sequence of jobs

        """
        Sequence = self.J[::-1]
        self.process(Sequence)
        return Sequence

    FIFO = FCFS
    LIFO = LCFS

    def SPT(self):
        """
        SPT (Shortest Processing Time) rule for scheduling.

        Returns: Sequence of jobs

        """
        if self.preced:
          Sequence=[]
          b = True
          G2=self.G.copy()
          while b:
            F=[]
            for i in G2:
              if list(G2.predecessors(i))==[]:
                F.append(i)
            p1={j:self.p[j] for j in F}
            P1=SingleMachineSP(len(F),F,p1)
            s=P1.SPT()
            G2.remove_nodes_from(F)
            if G2.number_of_nodes()==0:
              b=False
            Sequence=Sequence+s
        else:
          Sequence = [x for _, x in sorted(zip(self.p.values(), self.J))]
        self.process(Sequence)
        return Sequence

    def LPT(self):
      
        if self.preced:
          Sequence=[]
          b = True
          G2=self.G.copy()
          while b==True:
            F=[]
            D={}
            for i in  G2.nodes():
              if list( G2.predecessors(i))==[]:
                F.append(i)
                D[i]=G2.out_degree(i)
            p1={j:self.p[j] for j in F}
            P1=SingleMachineSP(len(F),F,p1,objective="Cmax")
            s=P1.LPT()
            G2.remove_nodes_from(F)
            if G2.number_of_nodes()==0:
              b=False
            Sequence=Sequence+s
        else:
          Sequence = [x for _, x in sorted(zip(zip(self.r.values(),[-k for k in self.p.values()]), self.J))]
        self.process(Sequence)
          
        return Sequence

    def WSPT(self):
        """
        WSPT (Weighted Shortest Processing Time) rule for scheduling.

        Returns: Sequence of jobs

        """
        rs = [x/y for x, y in zip(self.p.values(), self.w.values())]
        Sequence = [x for _, x in sorted(zip(zip(self.r.values(), rs), self.J))]
        self.process(Sequence)
        return Sequence

    def EDD(self):
        """
        EDD (Earliest Due Date) rule for scheduling.

        Returns: Sequence of jobs

        """
        if self.preced:
          Sequence=[]
          b = True
          G2=self.G.copy()
          while b:
            F=[]
            for i in G2:
              if list(G2.predecessors(i))==[]:
                F.append(i)
            p1={j:self.p[j] for j in F}
            d1={j:self.d[j] for j in F}
            P1=SingleMachineSP(len(F),F,p1,d=d1,objective="Cmax")
            s=P1.EDD()
            G2.remove_nodes_from(F)
            if G2.number_of_nodes()==0:
              b=False
            Sequence=Sequence+s
        else:
          Sequence = [x for _, x in sorted(zip(zip(self.r.values(),self.d.values()), self.J))]
        self.process(Sequence)
        return Sequence

    def LDD(self):
        """
        LDD (Latest Due Date) rule for scheduling.

        Returns: Sequence of jobs

        """
        if self.preced:
          Sequence=[]
          b = True
          G2=self.G.copy()
          while b:
            F=[]
            for i in G2:
              if list(G2.predecessors(i))==[]:
                F.append(i)
            p1={j:self.p[j] for j in F}
            d1={j:self.d[j] for j in F}
            P1=SingleMachineSP(len(F),F,p1,d=d1,objective="Cmax")
            s=P1.LDD()
            G2.remove_nodes_from(F)
            if G2.number_of_nodes()==0:
              b=False
            Sequence=Sequence+s
        else:
          Sequence = [x for _, x in sorted(zip(zip(self.r.values(),[-k for k in self.d.values()]), self.J))]
        self.process(Sequence)
        return Sequence

    def CR(self, check_time=False):
        """
        CR (Critical Ratio) rule for scheduling.

        Args:
          check_time: start time

        Returns: Sequence of jobs

        """
        if check_time == False:
            SyntaxError("check_time is not defined, Start time is used instead")
            check_time = self.start
        t = check_time
        CR = [(a-t)/b for a,b in zip(self.d.values(), self.p.values())]
        Sequence = [x for _, x in sorted(zip(CR, self.J))]
        self.process(Sequence)
        return Sequence
    CriticalRatio = CR

    def MinimumSlack(self, check_time=False):
        """
        Minimum Slack rule for scheduling.

        Args:
          check_time: start time

        Returns: Sequence of jobs

        """
        if check_time == False:
            SyntaxError("check_time is not defined, Start time is used instead")
            check_time = self.start
        t = check_time
        MS = [max(0,(a-t-b)) for a,b in zip(self.d.values(), self.p.values())]
        Sequence = [x for _, x in sorted(zip(MS, self.J))]
        self.process(Sequence)
        return Sequence
    MinSlack = MinimumSlack

    def MaximumSlack(self, check_time=False):
        """
        Maximum Slack rule for scheduling.

        Args:
          check_time: start time

        Returns: Sequence of jobs

        """
        if check_time == False:
            SyntaxError("check_time is not defined, Start time is used instead")
            check_time = self.start
        t = check_time
        MS = [max(0,(b-t-a)) for a,b in zip(self.d.values(), self.p.values())]
        Sequence = [x for _, x in sorted(zip(MS, self.J), reverse=True)]
        self.process(Sequence)
        return Sequence
    MaxSlack = MaximumSlack

    def ATC(self, check_time=False, K =False):
        """
        ATC (Apparent Tardiness Cost) rule for scheduling.

        Args:
          check_time: start time
          K: number of jobs to consider, default is 1

        Returns: Sequence of jobs

        """
        if check_time == False:
            SyntaxError("check_time is not defined, Start time is used instead")
            check_time = self.start
        if K == False:
            SyntaxError("K is not defined, K = 1 is used instead")
            K = 1
        t = check_time
        ATC = [0]*self.n
        P = sum(self.p.values())/self.n
        ATC=[(a/b)*exp(-max(c-t-b, 0)/(K*P)) for  a,b,c in zip(self.w.values(), self.p.values(),self.d.values())]
        Sequence = [x for _, x in sorted(zip(ATC, self.J), reverse=True)]
        self.process(Sequence)
        return Sequence

    def change2(self,s):
        """
        Randomly change two jobs in the sequence.

        Args:
          s: Sequence of jobs

        Returns: Sequence of jobs

        """
        sol=s
        j = random.randint(0,len(sol)-1)
        k=random.randint(0,len(sol)-1)
        while (k==j):
          k=random.randint(0,len(sol)-1)
        a=sol[k]
        b=sol[j]
        sol[j]=a
        sol[k]=b
        return sol

    def decrease(self,t,decreaseMethod,alpha):
        """
        Decrease the temperature.

        Args:
          t: temperature
          decreaseMethod: decrease method
          alpha: decrease parameter

        Returns: temperature

        """
        if decreaseMethod=='Geometric':
          return alpha*t
        if decreaseMethod=='Lineal':
          return t-alpha

    def SA(self,s,MaxIter,TemIni,decreaseMethod='Geometric',alpha=0.98):
        """

        Args:
          s: initial solution
          MaxIter: maximum number of iterations
          TemIni: initial temperature
          decreaseMethod: method to decrease temperature
          alpha: parameter to decrease temperature

        Returns: Sequence of jobs

        """
        Best=s
        self.process(s)
        c1=self.compute_objective(self.objective)
        cb=self.compute_objective(self.objective)
        k=0
        t=TemIni
        Val=[[k,c1,cb,0,(t/1000),s,Best]]
        while (k<MaxIter):
            k += 1
            R=self.change2(s)
            self.process(R)
            c2=self.compute_objective(self.objective)
            p=random.random()
            prob=[p,np.exp(-(c2-c1)/t)]
            if c2<c1 or p<np.exp(-(c2-c1)/t):
              s=R
              self.process(s)
              c1=self.compute_objective(self.objective)
            t=self.decrease(t,decreaseMethod,alpha);
            if c1<cb:
              Best=s.copy()
              self.process(Best)
              cb=self.compute_objective(self.objective)
            Val1=[k,c1,cb,prob[0],(t/1000),s,Best]
            Val.append(Val1)
        df=pd.DataFrame(Val)
        df
        x=df[0]
        y=df[1]
        plt.plot(x, y,linestyle='-')
        return Best

    def optimizationModel(self,problemName,objectiveFunction):
        """
        Optimization model for scheduling.

        Args:
          problemName: name of the problem
          objectiveFunction: objective function

        """
        self.objectiveFunction=objectiveFunction
        # Problem Definition
        self.problemSP=LpProblem(problemName,LpMinimize)
        #Decision Variables
        self.x=LpVariable.dicts('x',((j,k,i) for j in [0]+self.J for k in self.J for i in self.M if j!=k),lowBound=0,upBound=1,cat='Binary')
        self.c = LpVariable.dicts('c', iter([0]+self.J), lowBound=0, cat='Continuous')
        self.E = LpVariable.dicts('E', iter(self.J), lowBound=0, cat='Continuous')
        self.T = LpVariable.dicts('T', iter(self.J), lowBound=0, cat='Continuous')
        self.U = LpVariable.dicts('U', iter(self.J), lowBound=0, cat='Binary')
        self.cmax=LpVariable('cmax',cat='Continuous')
        self.Tmax=LpVariable('Tmax',cat='Continuous')
        self.Emax=LpVariable('Emax',cat='Continuous')
        # Objective function
        self.f0=LpAffineExpression(self.cmax)
        self.f1=LpAffineExpression(lpSum(self.c[j] for j in self.J)/self.n)
        self.f2=LpAffineExpression(lpSum(self.E[j] for j in self.J)/self.n)
        self.f3=LpAffineExpression(lpSum(self.T[j] for j in self.J)/self.n)
        self.f4=LpAffineExpression(lpSum(self.U[j] for j in self.J))
        self.f5=LpAffineExpression(lpSum(self.w[j]*self.c[j] for j in self.J))
        self.f6=LpAffineExpression(lpSum(self.w[j]*self.T[j] for j in self.J))
        self.f7=LpAffineExpression(lpSum(self.w[j]*self.E[j] for j in self.J))
        self.f8=LpAffineExpression(lpSum((self.w1[j]*self.E[j]+self.w2[j]*self.T[j]) for j in self.J))
        self.f9=LpAffineExpression(self.Tmax)
        self.f10=LpAffineExpression(self.Emax)
        if objectiveFunction =="Cmax":
          self.problemSP.setObjective(self.f0)
        if objectiveFunction == "AvgC":
          self.problemSP.setObjective(self.f1)
        if objectiveFunction == "AvgE":
          self.problemSP.setObjective(self.f2)
        if objectiveFunction == "AvgT":
          self.problemSP.setObjective(self.f3)
        if objectiveFunction == "MinTotalLateJobs":
          self.problemSP.setObjective(self.f4)
        if objectiveFunction == "WeightedC":
          self.problemSP.setObjective(self.f5)
        if objectiveFunction == "WeightedT":
          self.problemSP.setObjective(self.f6)
        if objectiveFunction == "WeightedE":
          self.problemSP.setObjective(self.f7)
        if objectiveFunction == "WeightedT+E":
          self.problemSP.setObjective(self.f8)
        if objectiveFunction == "Tmax":
          self.problemSP.setObjective(self.f9)
        if objectiveFunction == "Emax":
          self.problemSP.setObjective(self.f10)
        if objectiveFunction is None:
            print("No objective defined, the makespan will be minimized")
            self.problemSP.setObjective(self.f0)
        MM=sum(self.p.values())*10
        # Allocation constraints
        for k in self.J:
          self.problemSP+=lpSum(self.x[j,k,i] for i in self.M for j in [0]+self.J if j!=k)==1,'Al'+k
        for j in self.J:
          self.problemSP+=lpSum(self.x[j,k,i] for i in self.M for k in self.J if j!=k )<=1,'Al-1'+j
        for i in self.M:
          self.problemSP+=lpSum(self.x[0,k,i] for k in self.J)<=1,'Al-2'+i
        for i in self.M:
            for j in self.J:
                for k in self.J:
                    if j!=k:
                        self.problemSP += (
                            lpSum(
                                self.x[h, j, i]
                                for h in [0] + self.J
                                if h not in [k, j]
                            )
                            >= self.x[j, k, i]
                        )
        #earliness and tardiness constraints
        for j in self.J:
          self.problemSP+=self.c[j]==self.d[j]+self.T[j]-self.E[j],'EYT'+j
          self.problemSP+=self.T[j]<=self.U[j]*MM,'U'+j
          self.problemSP+=self.E[j]<=self.Emax
          self.problemSP+=self.T[j]<=self.Tmax
          self.problemSP+=self.c[j]<=self.cmax
        self.problemSP+=self.c[0]==0
        #non-interference constraints
        for i in self.M:
          for j in [0]+self.J:
            for k in self.J:
              if (j!=k):
                self.problemSP+=self.c[k]+MM*(1-self.x[j,k,i])>=self.c[j]+self.p[k]/self.v[i][k]
        # precedence constraints
        if self.preced==True:
          for (j,k) in self.prec:
              self.problemSP+=lpSum(self.x[j,k,i] for i in self.M)==1
              
    def optimizationModel2(self,problemName,objectiveFunction):
        """
        Optimization model for scheduling.

        Args:
          problemName: name of the problem
          objectiveFunction: objective function

        """
        self.objectiveFunction=objectiveFunction
        # Problem Definition
        self.problemSP=LpProblem(problemName,LpMinimize)
        #Decision Variables
        self.x=LpVariable.dicts('x',((j,i) for j in self.J for i in self.M),lowBound=0,upBound=1,cat='Binary')
        self.y=LpVariable.dicts('y',((u,v,i) for u in self.J for v in self.J for i in self.M),lowBound=0,upBound=1,cat='Binary')
        self.s = LpVariable.dicts('s', iter(self.J), lowBound=0, cat='Continuous')
        self.c = LpVariable.dicts('c', iter(self.J), lowBound=0, cat='Continuous')
        self.E = LpVariable.dicts('E', iter(self.J), lowBound=0, cat='Continuous')
        self.T = LpVariable.dicts('T', iter(self.J), lowBound=0, cat='Continuous')
        self.U = LpVariable.dicts('U', iter(self.J), lowBound=0, cat='Binary')
        self.cmax=LpVariable('cmax',cat='Continuous')
        self.Tmax=LpVariable('Tmax',cat='Continuous')
        self.Emax=LpVariable('Emax',cat='Continuous')
        # Objective function
        self.f0=LpAffineExpression(self.cmax)
        self.f1=LpAffineExpression(lpSum(self.c[j] for j in self.J)/self.n)
        self.f2=LpAffineExpression(lpSum(self.E[j] for j in self.J)/self.n)
        self.f3=LpAffineExpression(lpSum(self.T[j] for j in self.J)/self.n)
        self.f4=LpAffineExpression(lpSum(self.U[j] for j in self.J))
        self.f5=LpAffineExpression(lpSum(self.w[j]*self.c[j] for j in self.J))
        self.f6=LpAffineExpression(lpSum(self.w[j]*self.T[j] for j in self.J))
        self.f7=LpAffineExpression(lpSum(self.w[j]*self.E[j] for j in self.J))
        self.f8=LpAffineExpression(lpSum((self.w1[j]*self.E[j]+self.w2[j]*self.T[j]) for j in self.J))
        self.f9=LpAffineExpression(self.Tmax)
        self.f10=LpAffineExpression(self.Emax)
        if objectiveFunction =="Cmax":
          self.problemSP.setObjective(self.f0)
        if objectiveFunction == "AvgC":
          self.problemSP.setObjective(self.f1)
        if objectiveFunction == "AvgE":
          self.problemSP.setObjective(self.f2)
        if objectiveFunction == "AvgT":
          self.problemSP.setObjective(self.f3)
        if objectiveFunction == "MinTotalLateJobs":
          self.problemSP.setObjective(self.f4)
        if objectiveFunction == "WeightedC":
          self.problemSP.setObjective(self.f5)
        if objectiveFunction == "WeightedT":
          self.problemSP.setObjective(self.f6)
        if objectiveFunction == "WeightedE":
          self.problemSP.setObjective(self.f7)
        if objectiveFunction == "WeightedT+E":
          self.problemSP.setObjective(self.f8)
        if objectiveFunction == "Tmax":
          self.problemSP.setObjective(self.f9)
        if objectiveFunction == "Emax":
          self.problemSP.setObjective(self.f10)
        if objectiveFunction is None:
            print("No objective defined, the makespan will be minimized")
            self.problemSP.setObjective(self.f0)
        # Allocation constraints
        MM=sum(self.p.values())*10
        for j in self.J:
          self.problemSP+=lpSum(self.x[j,i] for i in self.M)==1,'Al'+j
        for i in self.M:
          self.problemSP+=lpSum((self.p[j]/self.v[i][j])*self.x[j,i] for j in self.J)<=self.cmax,'Al-2'+i
                

    def optimizationModel3(self,problemName,objectiveFunction):
        """
        Optimization model for scheduling.

        Args:
          problemName: name of the problem
          objectiveFunction: objective function

        """
        self.objectiveFunction=objectiveFunction
        # Problem Definition
        self.problemSP=LpProblem(problemName,LpMinimize)
        #Decision Variables
        self.x=LpVariable.dicts('x',((j,i) for j in self.J for i in self.M),lowBound=0,upBound=1,cat='Binary')
        self.y=LpVariable.dicts('y',((u,v,i) for u in self.J for v in self.J for i in self.M),lowBound=0,upBound=1,cat='Binary')
        self.s = LpVariable.dicts('s', iter(self.J), lowBound=0, cat='Continuous')
        self.c = LpVariable.dicts('c', iter(self.J), lowBound=0, cat='Continuous')
        self.E = LpVariable.dicts('E', iter(self.J), lowBound=0, cat='Continuous')
        self.T = LpVariable.dicts('T', iter(self.J), lowBound=0, cat='Continuous')
        self.U = LpVariable.dicts('U', iter(self.J), lowBound=0, cat='Binary')
        self.cmax=LpVariable('cmax',cat='Continuous')
        self.Tmax=LpVariable('Tmax',cat='Continuous')
        self.Emax=LpVariable('Emax',cat='Continuous')
        # Objective function
        self.f0=LpAffineExpression(self.cmax)
        self.f1=LpAffineExpression(lpSum(self.c[j] for j in self.J)/self.n)
        self.f2=LpAffineExpression(lpSum(self.E[j] for j in self.J)/self.n)
        self.f3=LpAffineExpression(lpSum(self.T[j] for j in self.J)/self.n)
        self.f4=LpAffineExpression(lpSum(self.U[j] for j in self.J))
        self.f5=LpAffineExpression(lpSum(self.w[j]*self.c[j] for j in self.J))
        self.f6=LpAffineExpression(lpSum(self.w[j]*self.T[j] for j in self.J))
        self.f7=LpAffineExpression(lpSum(self.w[j]*self.E[j] for j in self.J))
        self.f8=LpAffineExpression(lpSum((self.w1[j]*self.E[j]+self.w2[j]*self.T[j]) for j in self.J))
        self.f9=LpAffineExpression(self.Tmax)
        self.f10=LpAffineExpression(self.Emax)
        if objectiveFunction =="Cmax":
          self.problemSP.setObjective(self.f0)
        if objectiveFunction == "AvgC":
          self.problemSP.setObjective(self.f1)
        if objectiveFunction == "AvgE":
          self.problemSP.setObjective(self.f2)
        if objectiveFunction == "AvgT":
          self.problemSP.setObjective(self.f3)
        if objectiveFunction == "MinTotalLateJobs":
          self.problemSP.setObjective(self.f4)
        if objectiveFunction == "WeightedC":
          self.problemSP.setObjective(self.f5)
        if objectiveFunction == "WeightedT":
          self.problemSP.setObjective(self.f6)
        if objectiveFunction == "WeightedE":
          self.problemSP.setObjective(self.f7)
        if objectiveFunction == "WeightedT+E":
          self.problemSP.setObjective(self.f8)
        if objectiveFunction == "Tmax":
          self.problemSP.setObjective(self.f9)
        if objectiveFunction == "Emax":
          self.problemSP.setObjective(self.f10)
        if objectiveFunction is None:
            print("No objective defined, the makespan will be minimized")
            self.problemSP.setObjective(self.f0)
        # Allocation constraints
        MM=sum(self.p.values())*10
        for j in self.J:
          self.problemSP+=lpSum(self.x[j,i] for i in self.M)==1,'Al'+j

        #earliness and tardiness constraints
        for j in self.J:
          self.problemSP+=self.c[j]==self.s[j]+lpSum(self.x[j,i]*self.p[j]/self.v[i][j] for i in self.M)
          self.problemSP+=self.c[j]==self.d[j]+self.T[j]-self.E[j],'EYT'+j
          self.problemSP+=self.T[j]<=self.U[j]*MM,'U'+j
          self.problemSP+=self.E[j]<=self.Emax
          self.problemSP+=self.T[j]<=self.Tmax
          self.problemSP+=self.c[j]<=self.cmax
              
        for i in self.M:
          for v in self.J:
            for q in self.J:
              if (v!=q):
                self.problemSP+=self.c[v]<=self.s[q]+MM*(1-self.y[v,q,i])
        for i in self.M:
          for v in self.J:
            self.problemSP+=self.x[v,i]*MM>=lpSum(self.y[v,q,i]+self.y[q,v,i] for q in self.J)    
        for i in self.M:
          for v in self.J:
            for q in self.J:
              if (v!=q):
                self.problemSP+=self.y[v,q,i]+self.y[q,v,i]<=1
        for i in self.M:
          for v in self.J:
            for q in self.J:
              if (v!=q):
                self.problemSP+=MM*(self.y[v,q,i]+self.y[q,v,i])>=self.x[v,i]+self.x[q,i]-1
        # precedence constraints
        if self.preced==True:
          for (v,q) in self.prec:
            self.problemSP+=self.s[q]>=self.c[v]
                

    def showModel(self,filename):
          self.problemSP.writeLP(filename)

    def solve(self):
          """
          Solve the optimization problem.

          Returns: array of results.

          """
          self.problemSP.solve()
          print ("Status: ",LpStatus[self.problemSP.status])
          print("Objective Function (",self.objectiveFunction,") = ",self.problemSP.objective.value())
          results = [{'Job': k,'Machine': i,'Start': value(self.c[j]),'Duration': self.p[k]/self.v[i][k], 'Finish': value(self.c[k]), 'Due': self.d[k],'earliness': value(self.E[k]),'Tardiness': value(self.T[k])} for i in self.M for j in ([0]+self.J) for k in self.J if (j!=k and value(self.x[j,k,i])==1) ]
          schedule = pd.DataFrame(results)
          print('\nSchedule by Job')
          print(schedule.sort_values(by=['Job','Start']).set_index(['Job', 'Machine']))
          print('\nSchedule by Machine')
          print(schedule.sort_values(by=['Machine','Start']).set_index(['Machine', 'Job']))
          return results

    def solve2(self):
        """
          Solve the optimization problem version 2.

          Returns: array of results.

          """
        self.problemSP.solve()
        for j in self.J:
          print(j,value(self.s[j]),value(self.c[j]))
        for i in self.M:
          for j in self.J:
            print(i,j,value(self.x[j,i]))
          
        print ("Status: ",LpStatus[self.problemSP.status])
        cc = [[] for _ in range(self.m)]
        mac = [0 for _ in range(self.m)]
        for i in self.M:
          for j in self.J:
            if value(self.x[j,i])!=0:
              index=self.M.index(i)
              mac[index] = mac[index]+self.p[j]/self.v[self.M[index]][j]
              cc[index]=cc[index]+[j]
        results=self.process(sequence={},sequenceMach=cc)
        print("Objective Function (",self.objectiveFunction,") = ",self.problemSP.objective.value())
        schedule = pd.DataFrame(results)
        print('\nSchedule by Job')
        print(schedule.sort_values(by=['Job','Start']).set_index(['Job', 'Machine']))
        print('\nSchedule by Machine')
        print(schedule.sort_values(by=['Machine','Start']).set_index(['Machine', 'Job']))
        return results

    def solve3(self):
        """
          Solve the optimization problem version 2.

          Returns: array of results.

          """
        self.problemSP.solve()
        for j in self.J:
          print(j,value(self.s[j]),value(self.c[j]))
        for i in self.M:
          for j in self.J:
            print(i,j,value(self.x[j,i]))
          
        print ("Status: ",LpStatus[self.problemSP.status])
        cc = [[] for _ in range(self.m)]
        mac = [0 for _ in range(self.m)]
        for i in self.M:
          for j in self.J:
            if value(self.x[j,i])!=0:
              index=self.M.index(i)
              mac[index] = mac[index]+self.p[j]/self.v[self.M[index]][j]
              cc[index]=cc[index]+[j]
        results = [{'Job': j,'Machine': i,'Start': value(self.s[j]),'Duration': self.p[j]/self.v[i][j], 'Finish': value(self.c[j]), 'Due': self.d[j],'earliness': value(self.E[j]),'Tardiness': value(self.T[j])} for i in self.M for j in self.J if (value(self.x[j,i])==1) ]
        print("Objective Function (",self.objectiveFunction,") = ",self.problemSP.objective.value())
        schedule = pd.DataFrame(results)
        print('\nSchedule by Job')
        print(schedule.sort_values(by=['Job','Start']).set_index(['Job', 'Machine']))
        print('\nSchedule by Machine')
        print(schedule.sort_values(by=['Machine','Start']).set_index(['Machine', 'Job']))
        return results
        
class ProductionBalance:
    """

    Attributes:
    Mandatory attributes:
      n: number of jobs
      J: list of jobs
      p: processing times for each job
      R: list of relations between jobs
    Optional attributes:
      ct: cycle time, default False, if False, the minimum cycle time is computed
      ko: minimum number of stations, default False, if False, the minimum number of stations is computed
      Kmax: maximum number of stations, default False, if False, the maximum number of stations is computed
      objective: objective function, default None, if None, the cycle time is minimized
      gantt: show Gantt chart, if True gantt chart is shown, default False
      verbose: show verbose output, if True results are shown,  default False
    Other attributes:
      G: graph of the jobs
      EC: efficiency of cycle
      RB: balance delay
      TM: idle time
      objectiveFunction: objective function
      M: list of machines
      problemLB: optimization problem
      x: decision variables
      idle: decision variables
      kt: decision variables
      f0: objective function
      f1: objective function
      f2: objective function
    """

    def __init__(self, n , J, p, R, ct = False, ko = False, Kmax = False, objective = None, gantt = False, verbose = False):
        """

        Args:
        Attributes:
          n: number of jobs
          J: list of jobs
          p: processing times for each job
          R: list of relations between jobs
        Optional attributes:
          ct: cycle time, default False, if False, the minimum cycle time is computed
          ko: minimum number of stations, default False, if False, the minimum number of stations is computed
          Kmax: maximum number of stations, default False, if False, the maximum number of stations is computed
          objective: objective function, default None, if None, the cycle time is minimized
          gantt: show Gantt chart, if True gantt chart is shown, default False
          verbose: show verbose output, if True results are shown,  default False
        """
        self.n = n
        self.J = J
        self.p = p
        self.FF=[]
        self.R=R
        if ct == False and ko == False:
          print("The minimum cycle time is: ", max(self.p.values()))
          print("The maximum cycle time is: ", sum(self.p.values()) )
          print("You need to set the cycle time (ct) or minimum number of stations (ko)")
          input0 = input("Do you set the cycle time (ct) {Ans: Yes or Not}: ")
          if input0 == "Yes":
            ct11= int(input("Enter the cycle time (ct): "))
            if ct11<max(self.p.values()):
              print("The cycle time (ct) does not lower than ",max(self.p.values()))
              self.ct=max(self.p.values())
            else:
              self.ct=ct11
            ko1=np.ceil(sum(self.p.values())/self.ct)
            input2 = input("Now, Do you set the minimum number of stations (ko) {Ans: Yes or Not(ko is computed as "+ str(ko1)+" ) }: ")
            if input2 == "Yes":
              self.ko = int(input("Enter the minimum number of stations (ko): "))
            else:
              self.ko=ko1
              print( "The minimum number of stations (ko) is: ",self.ko)

          else:
            self.ko = int(input("Then, you need to set the minimum number of stations (ko) {Ans: integer}: "))
            ct_min=max(self.p.values())
            ct_c=sum(self.p.values())/self.ko
            self.ct=max(ct_min,ct_c)
            print("The  cycle time (ct) is: ", self.ct)

        else:
          if ko == False:
            self.ko=ceil(sum(self.p.values())/ct)
            print("The minimum number of stations is: ",self.ko)
          else:
            self.ko=ko
          if ct == False:
            ct_min=max(self.p.values())
            ct_c=sum(self.p.values())/self.ko
            self.ct=max(ct_min,ct_c)
            print("The cycle time is: ",self.ct)
          else:
            self.ct=ct
        #Input Data
        if Kmax == False:
          self.Kmax=len(self.J)
          print("The maximum number of stations is: ",self.Kmax)
        else:
          self.Kmax = Kmax
        #self.M=[f"Station{i+1}" for i in range(self.Kmax)]
        self.M=range(1,self.Kmax+1)
        print(self.M)
        self.objective=objective
        self.gantt = gantt
        self.verbose = verbose

        self.G = nx.DiGraph(list(self.R))
        if (set(self.J-self.G.nodes()))!=[]:
          for j in (set(self.J-self.G.nodes())):
            self.G.add_node(j)
        
        self.EC=sum(self.p.values())/(self.ko*self.ct)
        self.RB=1-self.EC
        self.TM=(self.ko*self.ct)-sum(self.p.values())
        print("Theoretical measures of performance")
        print("The Efficiency of cycle is: ", 100*self.EC," %.")
        print("The balance delay is: ", 100*self.RB," %.")
        print("The idle time is: ", self.TM)

    def visualize_Graph(self,results):
      """
      The `visualize_Graph` function creates a graph chart to visualize precedence relations and
      stations based on the input results.
      
      :param results: The `results` parameter in the `visualize_Graph` function is expected to be an
      array containing the results of a scheduling algorithm. This array likely contains information
      about jobs, machines, and possibly other scheduling-related data. The function then processes
      this data to create a graph chart that visualizes the
      :return: The `visualize_Graph` function returns a graph chart visualizing the precedence
      relations and stations based on the input results.
      """
      schedule = pd.DataFrame(results)
      JOBS = self.J
      MACHINES = sorted(list(schedule['Machine'].unique()))
      MA={schedule.loc[j,'Job']:schedule.loc[j,'Machine'] for j in range(len(schedule))}
      for layer, nodes in enumerate(nx.topological_generations(self.G)):
          for node in nodes:
              self.G.nodes[node]["layer"] = layer
      # Color mapping
      ColorLegend = {'Station'+str(i): i for i in MACHINES}
      values = [MA.get(node, 0) for node in self.G.nodes()]
      jet = cm = plt.get_cmap('jet')
      cNorm  = colors.Normalize(vmin=0, vmax=max(values))
      scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=jet)
      # Compute the multipartite_layout using the "layer" node attribute
      pos = nx.multipartite_layout(self.G, subset_key="layer")
      fig = plt.figure(1)
      ax = fig.add_subplot(1,1,1)
      for label in ColorLegend:
        ax.plot([0],[0],color=scalarMap.to_rgba(ColorLegend[label]),label=label)
      nx.draw_networkx(self.G,pos, cmap = jet, vmin=0, vmax= max(values),node_color=values,with_labels=True,ax=ax)
      ax.set_title("Example")
      plt.axis('off')
      fig.set_facecolor('w')
      plt.legend()
      fig.tight_layout()
      return plt.show()

    def SPT(self):
      """
      SPT (Shortest Processing Time) algorithm to allocate stations to jobs.
      Returns:
        results: array of results
        ctf: cycle time
        kf: number of stations

      """
      Sequence=[]
      stations=[]
      b = True
      stp=[]
      cp=0
      G2=self.G.copy()
      while b==True:
        F=[]
        for i in G2.nodes():
          if list(G2.predecessors(i))==[]:
            F.append(i)
        p1={j:self.p[j] for j in F}
        P1=SingleMachineSP(len(F),F,p1,objective='Cmax')
        s=P1.SPT()
        re=[s[0]]
        G2.remove_nodes_from(re)
        for j in re:
          if cp+p1[j]<=self.ct:
            cp=cp+p1[j]
            stp.append(j)
          else:
            stations.append(stp)
            stp=[]
            stp.append(j)
            cp=p1[j]
        if G2.number_of_nodes()==0:
          b=False
          stations.append(stp)
        Sequence=Sequence+[re]
      mac=len(stations)
      results = [{'Job': self.J[j],'Machine': self.M[i],'Start': 1,'Duration': self.p[self.J[j]]}  for i in range(mac) for j in range(len(self.J)) if self.J[j] in stations[i]]
      schedule = pd.DataFrame(results)
      print('\nSchedule by Job')
      print(schedule.sort_values(by=['Job','Start']).set_index(['Job', 'Machine']))
      print('\nSchedule by Machine')
      print(schedule.sort_values(by=['Machine','Start']).set_index(['Machine', 'Job']))
      ctf=self.ct
      kf=mac
      return results,ctf,kf

    def LPT(self):
      """
      LPT (Longest Processing Time) algorithm to allocate stations to jobs.
      Returns:
        results: array of results
        ctf: cycle time
        kf: number of stations

      """
      Sequence=[]
      stations=[]
      b = True
      stp=[]
      cp=0
      G2=self.G.copy()
      while b==True:
        F=[]
        for i in G2.nodes():
          if list(G2.predecessors(i))==[]:
            F.append(i)
        p1={j:self.p[j] for j in F}
        P1=SingleMachineSP(len(F),F,p1,objective='Cmax')
        s=P1.LPT()
        re=[s[0]]
        G2.remove_nodes_from(re)
        for j in re:
          if cp+p1[j]<=self.ct:
            cp=cp+p1[j]
            stp.append(j)
          else:
            stations.append(stp)
            stp=[]
            stp.append(j)
            cp=p1[j]
        if G2.number_of_nodes()==0:
          b=False
          stations.append(stp)
        Sequence=Sequence+[re]
      self.G = nx.DiGraph(list(self.R))
      mac=len(stations)
      results = [{'Job': self.J[j],'Machine': self.M[i],'Start': 1,'Duration': self.p[self.J[j]]}  for i in range(mac) for j in range(len(self.J)) if self.J[j] in stations[i]]
      schedule = pd.DataFrame(results)
      print('\nSchedule by Job')
      print(schedule.sort_values(by=['Job','Start']).set_index(['Job', 'Machine']))
      print('\nSchedule by Machine')
      print(schedule.sort_values(by=['Machine','Start']).set_index(['Machine', 'Job']))
      ctf=self.ct
      kf=mac
      return results,ctf,kf

    def SINS(self):
      """
      LPT (Longest Processing Time) algorithm to allocate stations to jobs.
      Returns:
        results: array of results
        ctf: cycle time
        kf: number of stations

      """
      Sequence=[]
      stations=[]
      b = True
      stp=[]
      cp=0
      while b==True:
        F=[]
        D={}
        for i in self.G.nodes():
          if list(self.G.predecessors(i))==[]:
            F.append(i)
            D[i]=self.G.out_degree(i)
        p1={j:self.p[j] for j in F}
        p2={j:D[j] for j in F}
        print(p1)
        P1=SingleMachineSP(len(F),F,p2)
        s=P1.SPT()
        re=[s[0]]
        self.G.remove_nodes_from(re)
        for j in re:
          if cp+p1[j]<=self.ct:
            cp=cp+p1[j]
            stp.append(j)
          else:
            stations.append(stp)
            stp=[]
            stp.append(j)
            cp=p1[j]
        if self.G.number_of_nodes()==0:
          b=False
          stations.append(stp)

        Sequence=Sequence+[re]
      self.G = nx.DiGraph(list(self.R))
      mac=len(stations)
      results = [{'Job': self.J[j],'Machine': self.M[i],'Start': 1,'Duration': self.p[self.J[j]]}  for i in range(mac) for j in range(len(self.J)) if self.J[j] in stations[i]]
      schedule = pd.DataFrame(results)
      print('\nSchedule by Job')
      print(schedule.sort_values(by=['Job','Start']).set_index(['Job', 'Machine']))
      print('\nSchedule by Machine')
      print(schedule.sort_values(by=['Machine','Start']).set_index(['Machine', 'Job']))
      ctf=self.ct
      kf=mac
      return results,ctf,kf

    def LINS(self):
      """
      LPT (Longest Processing Time) algorithm to allocate stations to jobs.
      Returns:
        results: array of results
        ctf: cycle time
        kf: number of stations

      """
      Sequence=[]
      stations=[]
      b = True
      stp=[]
      cp=0
      while b==True:
        F=[]
        D={}
        for i in self.G.nodes():
          if list(self.G.predecessors(i))==[]:
            F.append(i)
            D[i]=self.G.out_degree(i)
        p1={j:self.p[j] for j in F}
        p2={j:D[j] for j in F}
        print(p1)
        P1=SingleMachineSP(len(F),F,p2)
        s=P1.LPT()
        re=[s[0]]
        self.G.remove_nodes_from(re)
        for j in re:
          if cp+p1[j]<=self.ct:
            cp=cp+p1[j]
            stp.append(j)
          else:
            stations.append(stp)
            stp=[]
            stp.append(j)
            cp=p1[j]
        if self.G.number_of_nodes()==0:
          b=False
          stations.append(stp)
        Sequence=Sequence+[re]
      self.G = nx.DiGraph(list(self.R))
      mac=len(stations)
      results = [{'Job': self.J[j],'Machine': self.M[i],'Start': 1,'Duration': self.p[self.J[j]]}  for i in range(mac) for j in range(len(self.J)) if self.J[j] in stations[i]]
      schedule = pd.DataFrame(results)
      print('\nSchedule by Job')
      print(schedule.sort_values(by=['Job','Start']).set_index(['Job', 'Machine']))
      print('\nSchedule by Machine')
      print(schedule.sort_values(by=['Machine','Start']).set_index(['Machine', 'Job']))
      ctf=self.ct
      kf=mac
      return results,ctf,kf

    def PW(self):
      """
      LPT (Longest Processing Time) algorithm to allocate stations to jobs.
      Returns:
        results: array of results
        ctf: cycle time
        kf: number of stations
      """
      G1=self.G.copy()
      suc=()
      for i in G1.nodes():
          if list(self.G.successors(i))==[]:
            suc=((i,"End"),)+suc            
      print(G1.edges())  
      print(suc)
      G1.add_edges_from(list(suc))
      print(G1.edges())  
      pw={o: max([sum([self.p[i] for i in q if i !="End"]) for q in nx.all_simple_paths(G1,o,"End")]) for o in self.J}
      print("PW",pw)
      G2=self.G.copy()
      Sequence=[]
      stations=[]
      b = True
      stp=[]
      cp=0
      while b==True:
        F=[]
        for i in G2.nodes():
          if list(G2.predecessors(i))==[]:
            F.append(i)
        p1={j:self.p[j] for j in F}
        p2={j:pw[j] for j in F}
        P1=SingleMachineSP(len(F),F,p2,objective='Cmax')
        s=P1.LPT()
        re=[s[0]]
        G2.remove_nodes_from(re)
        for j in re:
          if cp+p1[j]<=self.ct:
            cp+=p1[j]
            stp.append(j)
          else:
            stations.append(stp)
            stp=[]
            stp.append(j)
            cp=p1[j]
        if G2.number_of_nodes()==0:
          b=False
          stations.append(stp)
        Sequence=Sequence+[re]
      #self.G = nx.DiGraph(list(self.R))
      mac=len(stations)
      results = [{'Job': self.J[j],'Machine': self.M[i],'Start': 1,'Duration': self.p[self.J[j]]}  for i in range(mac) for j in range(len(self.J)) if self.J[j] in stations[i]]
      schedule = pd.DataFrame(results)
      print('\nSchedule by Job')
      print(schedule.sort_values(by=['Job','Start']).set_index(['Job', 'Machine']))
      print('\nSchedule by Machine')
      print(schedule.sort_values(by=['Machine','Start']).set_index(['Machine', 'Job']))
      ctf=self.ct
      kf=mac
      return results,ctf,kf

    def sPW(self):
      """
      LPT (Longest Processing Time) algorithm to allocate stations to jobs.
      Returns:
        results: array of results
        ctf: cycle time
        kf: number of stations
      """
      G1=self.G.copy()
      suc=()
      for i in G1.nodes():
          if list(self.G.successors(i))==[]:
            suc=((i,"End"),)+suc            
      print(G1.edges())  
      print(suc)
      G1.add_edges_from(list(suc))
      print(G1.edges())  
      pw={o: max([sum([self.p[i] for i in q if i !="End"]) for q in nx.all_simple_paths(G1,o,"End")]) for o in self.J}
      print("PW",pw)
      G2=self.G.copy()
      Sequence=[]
      stations=[]
      b = True
      stp=[]
      cp=0
      while b==True:
        F=[]
        for i in G2.nodes():
          if list(G2.predecessors(i))==[]:
            F.append(i)
        p1={j:self.p[j] for j in F}
        p2={j:pw[j] for j in F}
        P1=SingleMachineSP(len(F),F,p2,objective='Cmax')
        s=P1.SPT()
        re=[s[0]]
        G2.remove_nodes_from(re)        
        
        for j in re:
          if cp+p1[j]<=self.ct:
            cp+=p1[j]
            stp.append(j)
          else:
            stations.append(stp)
            stp=[]
            stp.append(j)
            cp=p1[j]
        if G2.number_of_nodes()==0:
          b=False
          stations.append(stp)
        Sequence=Sequence+[re]
      #self.G = nx.DiGraph(list(self.R))
      mac=len(stations)
      results = [{'Job': self.J[j],'Machine': self.M[i],'Start': 1,'Duration': self.p[self.J[j]]}  for i in range(mac) for j in range(len(self.J)) if self.J[j] in stations[i]]
      schedule = pd.DataFrame(results)
      print('\nSchedule by Job')
      print(schedule.sort_values(by=['Job','Start']).set_index(['Job', 'Machine']))
      print('\nSchedule by Machine')
      print(schedule.sort_values(by=['Machine','Start']).set_index(['Machine', 'Job']))
      ctf=self.ct
      kf=mac
      return results,ctf,kf


    def optimizationModel(self,problemName,objectiveFunction):
        """
        Create the optimization model.
        Args:
          problemName: name of the problem
          objectiveFunction: objective function
        Returns:
          problemLB: optimization problem
        """
        self.objectiveFunction=objectiveFunction
        # Problem Definition
        self.M=range(1,self.Kmax+1)
        cost={i:{j:0 for j in self.p.keys()}for i in self.M}
        self.FF=[]
        for i in self.G.nodes():
            if not list(self.G.successors(i)): self.FF.append(i)
        for j, i in itertools.product(self.FF, range(self.ko+1,self.Kmax+1)):
            f = sum(self.p[h] for h in self.FF)
            cost[i][j]=self.p[j]*((f+1)**(i-self.ko+1))

        MM=sum(self.p.values())*100
        self.problemLB=LpProblem(problemName,LpMinimize)
        #Decision Variables
        self.x = LpVariable.dicts('x', ((i, j) for j in self.J for i in self.M ), lowBound=0, upBound=1, cat='Binary')
        self.y = LpVariable.dicts('y', iter(self.M), lowBound=0, upBound=1, cat='Binary')
        self.idle = LpVariable.dicts('id', iter(self.M), lowBound=0, cat='Continuous')
        self.kt =  LpVariable('kmachines', lowBound=0, cat='Integer')
        self.ctt = LpVariable('CycleTime',lowBound=0, cat='Continuous')
        #Objective Function
        self.f0=LpAffineExpression(lpSum(cost[i][j]*self.x[i,j] for i in self.M for j in self.J)+lpSum(self.y[i] for i in self.M))
        self.f1=LpAffineExpression(self.kt)
        self.f2=LpAffineExpression(lpSum(self.idle[i] for i in self.M))
        self.f3=LpAffineExpression(self.ctt)
        if self.objectiveFunction =="Mincost":
          self.problemLB.setObjective(self.f0)
        if self.objectiveFunction == "Min K":
          self.problemLB.setObjective(self.f1)
        if self.objectiveFunction == "Min idle":
          self.problemLB.setObjective(self.f2)
        if self.objectiveFunction == "Min ct":
          self.problemLB.setObjective(self.f3)
        if self.objectiveFunction is None:
          print("No objective defined, the cost will be minimized")
          self.problemSP.setObjective(self.f0)
        # Cycle time constraints
        if self.objectiveFunction == "Min ct":
          for i in self.M:
            self.problemLB+=lpSum(self.x[i,j]*self.p[j] for j in self.J)+self.idle[i]==self.ctt          
            self.problemLB+=lpSum(self.x[i,j]*self.p[j] for j in self.J)<=MM*self.y[i]
            
        else:
          for i in self.M:
            self.problemLB+=lpSum(self.x[i,j]*self.p[j] for j in self.J)+self.idle[i]==self.ct*self.y[i]
        # Allocation constraints
        for j in self.J:
            self.problemLB += lpSum(self.x[i,j] for i in self.M) <= 1
        self.problemLB+= -self.n+lpSum(self.x[i,j] for i in self.M for j in self.J)>=0
        # Precedence constraints
        for (u,v) in self.R:
          self.problemLB+=lpSum((self.Kmax-i+1)*(self.x[i,v]-self.x[i,u])for i in self.M)<=0
        # Minimum number of stations constraints
        self.problemLB+=lpSum(self.y[i] for i in self.M) ==self.kt
        #print(self.problemLB)

    def showModel(self,filename):
          """
          Show the model.
          Args:
            filename: name of the file
          Returns: file with the model
          """
          self.problemLB.writeLP(filename)

    def solve(self):
          """
          Solve the optimization problem.
          Returns:
            results: array of results
            ctf: cycle time
            kf: number of stations

          """
          self.problemLB.solve()
          print ("Status: ",LpStatus[self.problemLB.status])
          print("Objective Function (",self.objectiveFunction,") = ",self.problemLB.objective.value())
          results = [{'Job': j,'Machine': i,'Start': value(self.x[i,j]),'Duration': self.p[j]}  for j in self.J for i in self.M if value(self.x[i,j])==1]
          schedule = pd.DataFrame(results)
          print('\nSchedule by Job')
          print(schedule.sort_values(by=['Job','Start']).set_index(['Job', 'Machine']))
          print('\nSchedule by Machine')
          print(schedule.sort_values(by=['Machine','Start']).set_index(['Machine', 'Job']))
          if self.objectiveFunction=="Min ct":
            ctf=value(self.ctt)
          else:  
            ctf=self.ct
          kf=value(lpSum(self.y[i] for i in self.M))
          return results,ctf,kf

    def performance(self,results,ctf,kf):
        """
        Calculate the performance of the solution.
        Args:
          results: array of results
          ctf: cycle time
          kf: number of stations
        """
        schedule = pd.DataFrame(results)
        self.EC=sum(self.p.values())/(kf*ctf)
        self.RB=1-self.EC
        self.TM=(kf*ctf)-sum(self.p.values())
        print("Theoretical measures of performance")
        print("The Efficiency of cycle is: ", 100*self.EC," %.")
        print("The balance delay is: ", 100*self.RB," %.")
        print("The idle time is: ", self.TM)
        print('\nEfficiency')
        print(schedule.groupby('Machine')['Duration'].sum()*100/ctf)
        print('\nBalance Delay')
        print(100-schedule.groupby('Machine')['Duration'].sum()*100/ctf)
        print('\n idle Time')
        print(ctf-schedule.groupby('Machine')['Duration'].sum())


class ProductionLine:
    """A class used to represent a production line.

    Methods can be called to describe the
    characteristics of the production line using
    Factory Physics laws and definitions.

    Attributes
    M : set
        The set of stations.
    p: dictionary
        The processing time of each station.
    m: dictionary
        The number of machines of each station.
    r_b : number
        The bottleneck rate. It is the rate of the
        workstation having the highest long-term utilization.
        Uses units of parts per unit time.
    T_0 : number
        The natural process time. It is the sum of the
        long-term average process times of each workstation in
        the line. Uses units of time.
    name : string
        The name of the production line.

    """

    def __init__(self, M, p, m = {}, name=None):

        self.M = M
        self.m = {i:1 for i in self.M} if m == {} else m
        self.p=p
        
        self.rate ={i:self.m[i]/self.p[i] for i in self.M} 
        print(self.rate)
        self.bn = min(self.rate, key=self.rate.get)
        self.r_b = min(self.rate.values())
        self.T_0 = sum(self.p.values())
        self.W_0 = self.r_b * self.T_0
        self._name = name
        print("The bottleneck rate (r_b) is : ",np.round(self.r_b,2))
        print("The critical work in process (W_o) is: ", np.round(self.W_0,2))
        print("The critical cycle time (T_o) is: ", self.T_0)
        

    @property
    def name(self):
        return self._name

    def CT_best(self, w):
        """Returns the minimum cycle time for a given WIP level w.

        Describes the relationship between WIP and cycle time
        for a perfect line with no variability.

        Factory Physics 3e, p.241

        Args:
          w: number
            The WIP level.

        Returns:
          number
            The cycle time.
        """
        return self.T_0 if w <= self.W_0 else w / self.r_b


    def TH_best(self, w):
        """Returns the maximum throughput for a given WIP level w.

        Describes the relationship between WIP and cycle time
        for a perfect line with no variability.

        Factory Physics 3e, p.241
        Args:
          w: number
            The WIP level.

        Returns:
          number
            The throughput.
        """

        return w / self.T_0 if w <= self.W_0 else self.r_b


    # Law (Worst-Case Performance) p.243
    def CT_worst(self, w):
        """Returns the worst-case cycle time for a given WIP level w.

        Describes the relationship between WIP and cycle time
        for a line with maximum variability.

        Factory Physics 3e, p.243

        Args:
          w: number
            The WIP level.

        Returns:
          number
            The cycle time.
        """

        return w * self.T_0


    def TH_worst(self):
        """Returns the worst-case throughput for a given WIP level w.

        Describes the relationship between WIP and cycle time
        for a line with maximum variability.

        Factory Physics 3e, p.243

        Returns:
          number
            The throughput.
        """

        return 1 / self.T_0


    # Definition (Practical Worst-Case Performance) p.247
    def CT_PWC(self, w):
        """Returns the practical worst-case cycle time for a given WIP level w.

        Describes the relationship between WIP and cycle time
        for a line with "maximum randomness".

        Factory Physics 3e, p.247
        Args:
          w: number
            The WIP level.

        Returns:
          number
            The cycle time.
        """

        return self.T_0 + (w - 1) / self.r_b


    def TH_PWC(self, w):
        """Returns the practical worst-case throughput for a given WIP level w.

        Describes the relationship between WIP and cycle time
        for a line with "maximum randomness".

        Factory Physics 3e, p.247

        Args:
          w: number
            The WIP level.

        Returns:
          number
            The throughput.
        """

        return  (w / (self.W_0 + w - 1)) * self.r_b


    def df_scenarios(self,ProductionLine,max_wip):
        """Creates a DataFrame of the best case, worst case, and practical worst case
        of throughput and cycle time for the ProductionLine object provided.

        Args:
          ProductionLine: ProductionLine object
          max_wip: number
            The maximum WIP level.

        Returns:
          DataFrame
        """
        df = pd.DataFrame(index=np.arange(1,max_wip+1)) # +1 is to include the WIP level entered.
        df['WIP'] = df.index
        df['TH Best Case'] = df['WIP'].apply(ProductionLine.TH_best)
        df['TH Worst Case'] = ProductionLine.TH_worst()
        df['TH Practical Worst Case'] = df['WIP'].apply(ProductionLine.TH_PWC)
        df['CT Best Case'] = df['WIP'].apply(ProductionLine.CT_best)
        df['CT Worst Case'] = df['WIP'].apply(ProductionLine.CT_worst)
        df['CT Practical Worst Case'] = df['WIP'].apply(ProductionLine.CT_PWC)
        return df

    def plot_scenarios_TH(self,ProductionLine,df,max_wip):
        """Creates a plot of the best case, worst case, and practical worst case
        of throughput and cycle time for the ProductionLine object provided.

        Args:
          ProductionLine: ProductionLine object
          max_wip: number
            The maximum WIP level.

        Returns:
          Plot
        """
        fig = go.Figure()

        # Horizontal line for r_b
        fig.add_shape(type="line",x0=0,y0=ProductionLine.r_b,x1=df['WIP'].max(),y1=ProductionLine.r_b,line=dict(color="black",width=1,dash="dash",))

        # Horizontal line for T_0
        fig.add_shape(type="line",x0=0,y0=1/ProductionLine.T_0,x1=df['WIP'].max(),y1=1/ProductionLine.T_0,line=dict(color="black",width=1,dash="dash",))

        # Create and style traces
        fig.add_trace(go.Scatter(x=df['WIP'], y=df['TH Practical Worst Case'], name='Practical Worst Case'))
        fig.add_trace(go.Scatter(x=df['WIP'], y=df['TH Worst Case'], name='Worst Case'))
        fig.add_trace(go.Scatter(x=df['WIP'], y=df['TH Best Case'], name = 'Best Case'))

        # Set axes ranges
        fig.update_xaxes(range=[0, df['WIP'].max()])
        fig.update_yaxes(range=[0,df['TH Best Case'].max()*1.5])

        # Edit the layout
        fig.update_layout(title=f'Throughput Time vs WIP for {ProductionLine._name}',
                        xaxis_title='WIP',
                        yaxis_title='Throughput (parts/unit time)')

        fig.update_layout(
            showlegend=True,
            annotations=[
                dict(
                    x=2.5,
                    y=ProductionLine.r_b,
                    xref="x",
                    yref="y",
                    text="Bottleneck Rate (r_b)",
                    showarrow=True,
                    arrowhead=7,
                    ax=0,
                    ay=-40)])

        return fig.show()
      
    def plot_scenarios_CT(self,ProductionLine,df,max_wip):
        """Creates a plot of the best case, worst case, and practical worst case
        of throughput and cycle time for the ProductionLine object provided.

        Args:
          ProductionLine: ProductionLine object
          max_wip: number
            The maximum WIP level.

        Returns:
          Plot
        """
        fig = go.Figure()

        # Horizontal line for r_b
#        fig.add_shape(type="line",x0=0,y0=ProductionLine.r_b,x1=df['WIP'].max(),y1=ProductionLine.r_b,line=dict(color="black",width=1,dash="dash",))

        # Horizontal line for T_0
        fig.add_shape(type="line",x0=0,y0=ProductionLine.T_0,x1=df['WIP'].max(),y1=ProductionLine.T_0,line=dict(color="black",width=1,dash="dash",))

        # Create and style traces
        fig.add_trace(go.Scatter(x=df['WIP'], y=df['CT Practical Worst Case'], name='Practical Worst Case'))
        fig.add_trace(go.Scatter(x=df['WIP'], y=df['CT Worst Case'], name='Worst Case'))
        fig.add_trace(go.Scatter(x=df['WIP'], y=df['CT Best Case'], name = 'Best Case'))

        # Set axes ranges
        fig.update_xaxes(range=[0, df['WIP'].max()])
        fig.update_yaxes(range=[0,df['CT Best Case'].max()*1.5])

        # Edit the layout
        fig.update_layout(title=f'Cycle Time vs WIP for {ProductionLine._name}',
                        xaxis_title='WIP',
                        yaxis_title='Cycle time (unit time)')

        fig.update_layout(
            showlegend=True,
            annotations=[
                dict(
                    x=0,
                    y=ProductionLine.T_0,
                    xref="x",
                    yref="y",
                    text="Critical Cycle Time (T_0)",
                    showarrow=True,
                    arrowhead=0,
                    ax=0,
                    ay=-40)])

        return fig.show()
      
    def plot_production_line(self,ProductionLine):
        # Crear la figura y los ejes
        fig, ax = plt.subplots()

        # Dibujar una línea base que representa la línea de producción
        ax.plot([0, 4*len(ProductionLine.M)], [1, 1], color='black', linewidth=1)

        # Definir las posiciones de las estaciones en la línea
        estaciones_pos = {ProductionLine.M[i]:1.5 +i*4 for i in range(len(ProductionLine.M))}
        
        # Dibujar las estaciones como rectángulos
        for i in ProductionLine.M:
            if i==ProductionLine.bn:
                rect = mpatches.Rectangle((estaciones_pos[i] - 1, 0.5), 3, 1, edgecolor='black', facecolor='red')
            else:
              rect = mpatches.Rectangle((estaciones_pos[i] - 1, 0.5), 3, 1, edgecolor='black', facecolor='lightblue')
            ax.add_patch(rect)
            ax.text(estaciones_pos[i]+0.5, 1.5, i, ha='center', fontsize=10)
            ax.text(estaciones_pos[i]+0.5, 1.4, f'r({i})={np.round(ProductionLine.rate[i],2)}', ha='center', fontsize=9)
            ax.text(estaciones_pos[i]+0.5, 1.3, f'm({i})={ProductionLine.m[i]}', ha='center', fontsize=9)
            ax.text(estaciones_pos[i]+0.5, 1.2, f'p({i})={ProductionLine.p[i]}', ha='center', fontsize=9)
        

        # Quitar los ejes
        ax.axis('off')
        plt.title(f'Line Representation of {ProductionLine._name}')
        # Mostrar el dibujo
        
        plt.show()

      