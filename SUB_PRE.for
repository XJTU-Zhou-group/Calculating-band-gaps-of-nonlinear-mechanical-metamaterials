      SUBROUTINE MPC(UE,A,JDOF,MDOF,N,JTYPE,X,U,UINIT,MAXDOF,LMPC,
     * KSTEP,KINC,TIME,NT,NF,TEMP,FIELD,LTRAN,TRAN)
      INCLUDE 'ABA_PARAM.INC'
      DIMENSION UE(MDOF),A(MDOF,MDOF,N),JDOF(MDOF,N),X(6,N),
     * U(MAXDOF,N),UINIT(MAXDOF,N),TIME(2),TEMP(NT,N),
     * FIELD(NF,NT,N),LTRAN(N),TRAN(3,3,N)

      PUT THE VARIABLES HERE

      IF (KSTEP-1 < 21) THEN
           INK1=INT(KSTEP-1)
           INK2=0
      ELSE IF (KSTEP-1 < 41) THEN
           INK1=20
           INK2=INT(KSTEP-21)
      ELSE IF (KSTEP-1 < 61) THEN
           INK1=61-KSTEP
           INK2=61-KSTEP
      ENDIF

      A=0.d00
      var1=CEILING(JTYPE/2.000000e+000)
      var2=FLOOR(JTYPE/2.000000e+000)

      IF (var2 .EQ. 5) THEN
           IF (KSTEP .EQ. 1) THEN
                LMPC=1
           ELSE
                LMPC=0
           ENDIF
           JDOF(1,1)=1
           JDOF(1,2)=1
           JDOF(1,3)=1
           A(1,1,1)=1.d00
           A(1,1,2)=-1.d00
           A(1,1,3)=-1.d00
           A(1,1,3)=-(X(1,1)-X(1,2))
           JDOF(2,1)=2
           JDOF(2,2)=2
           JDOF(2,3)=2
           A(2,2,1)=1.d00
           A(2,2,2)=-1.d00
           A(2,2,3)=-1.d00
           A(2,2,3)=-(X(2,1)-X(2,2))
      ELSE
           IF (var1 .EQ. var2) THEN
                IF (KSTEP .EQ. 1) THEN
                     LMPC=0
                     INK0=1
                ELSE
                     LMPC=1
                ENDIF
                IF (var1 .EQ. 1) THEN
                     INK0=INK1
                ELSE
                     INK0=INK2
                ENDIF
c                Rval=RA(JTYPE,1)*RK0(INK0,1)
                Rval=RA(1,1)*RK0(INK0,1)
                JDOF(1,1)=1
                JDOF(1,2)=1
                JDOF(1,3)=1
                A(1,1,1)=1.d00
                A(1,1,2)=SIN(Rval)
                A(1,1,3)=-COS(Rval)
                JDOF(2,1)=2
                JDOF(2,2)=2
                JDOF(2,3)=2
                A(2,2,1)=1.d00
                A(2,2,2)=SIN(Rval)
                A(2,2,3)=-COS(Rval)
           ELSE
                IF (KSTEP .EQ. 1) THEN
                     LMPC=0
                     INK0=1
                ELSE
                     LMPC=1
                ENDIF
                IF (var1 .EQ. 1) THEN
                     INK0=INK1
                ELSE
                     INK0=INK2
                ENDIF
c                Rval=RA(JTYPE,1)*RK0(INK0,1)
                Rval=RA(1,1)*RK0(INK0,1)
                JDOF(1,1)=1
                JDOF(1,2)=1
                JDOF(1,3)=1
                A(1,1,1)=1.d00
                A(1,1,2)=-COS(Rval)
                A(1,1,3)=-SIN(Rval)
                JDOF(2,1)=2
                JDOF(2,2)=2
                JDOF(2,3)=2
                A(2,2,1)=1.d00
                A(2,2,2)=-COS(Rval)
                A(2,2,3)=-SIN(Rval)
           ENDIF
      ENDIF
      RETURN
      END