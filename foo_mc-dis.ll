; ModuleID = 'foo_mc'
source_filename = "foo_mc"

@rodata_15 = private unnamed_addr constant [62 x i8] c"\01\00\02\00hello world\0A\00hello world_2\0A\00Basic Block : %s\0A\00Energy: 15\0A\00", align 4, !ROData_SecInfo !0

declare dso_local i32 @printf(i8*, ...)

define dso_local i32 @hello() {
entry:
  %RSP_P.0 = alloca i64, align 1
  store i64 3735928559, i64* %RSP_P.0, align 8
  %RBP = ptrtoint i64* %RSP_P.0 to i64
  %EAX = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([62 x i8], [62 x i8]* @rodata_15, i32 0, i32 4))
  ret i32 %EAX
}

define dso_local i32 @main() {
entry:
  %stktop_8 = alloca i8, i32 24, align 1
  %RSPAdj_N.16 = bitcast i8* %stktop_8 to i64*
  %0 = getelementptr i8, i8* %stktop_8, i64 16
  %RBP_N.8 = bitcast i8* %0 to i32*
  %1 = getelementptr i8, i8* %stktop_8, i64 20
  %RBP_N.4 = bitcast i8* %1 to i32*
  %2 = getelementptr i8, i8* %stktop_8, i64 0
  %RSP_P.0 = bitcast i8* %2 to i64*
  store i64 3735928559, i64* %RSP_P.0, align 8
  %RBP = ptrtoint i64* %RSP_P.0 to i64
  store i32 0, i32* %RBP_N.4, align 1
  store i32 9, i32* %RBP_N.8, align 1
  %3 = load i32, i32* %RBP_N.8, align 1
  %4 = zext i32 %3 to i64
  %5 = zext i32 2 to i64
  %6 = sub i64 %4, %5
  %7 = call { i64, i1 } @llvm.usub.with.overflow.i64(i64 %4, i64 %5)
  %CF = extractvalue { i64, i1 } %7, 1
  %ZF = icmp eq i64 %6, 0
  %highbit = and i64 -9223372036854775808, %6
  %SF = icmp ne i64 %highbit, 0
  %8 = call { i64, i1 } @llvm.ssub.with.overflow.i64(i64 %4, i64 %5)
  %OF = extractvalue { i64, i1 } %8, 1
  %9 = and i64 %6, 255
  %10 = call i64 @llvm.ctpop.i64(i64 %9)
  %11 = and i64 %10, 1
  %PF = icmp eq i64 %11, 0
  %CmpZF_JLE = icmp eq i1 %ZF, true
  %CmpOF_JLE = icmp ne i1 %SF, %OF
  %ZFOrSF_JLE = or i1 %CmpZF_JLE, %CmpOF_JLE
  br i1 %ZFOrSF_JLE, label %bb.2, label %bb.1

bb.1:                                             ; preds = %entry
  %EAX = call i32 @hello()
  br label %bb.3

bb.2:                                             ; preds = %entry
  %EAX1 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([62 x i8], [62 x i8]* @rodata_15, i32 0, i32 17))
  br label %bb.3

bb.3:                                             ; preds = %bb.2, %bb.1
  ret i32 0
}

define dso_local i32 @print(i64 %arg1) {
entry:
  %stktop_8 = alloca i8, i32 24, align 1
  %RSPAdj_N.16 = bitcast i8* %stktop_8 to i64*
  %0 = getelementptr i8, i8* %stktop_8, i64 16
  %RBP_N.8 = bitcast i8* %0 to i64*
  %1 = getelementptr i8, i8* %stktop_8, i64 0
  %RSP_P.0 = bitcast i8* %1 to i64*
  store i64 3735928559, i64* %RSP_P.0, align 8
  %RBP = ptrtoint i64* %RSP_P.0 to i64
  store i64 %arg1, i64* %RBP_N.8, align 1
  %memload = load i64, i64* %RBP_N.8, align 1
  %EAX = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([62 x i8], [62 x i8]* @rodata_15, i32 0, i32 32), i64 %memload)
  %EAX1 = call i32 (i8*, ...) @printf(i8* getelementptr inbounds ([62 x i8], [62 x i8]* @rodata_15, i32 0, i32 50))
  ret i32 %EAX1
}

; Function Attrs: nocallback nofree nosync nounwind readnone speculatable willreturn
declare { i64, i1 } @llvm.usub.with.overflow.i64(i64, i64) #0

; Function Attrs: nocallback nofree nosync nounwind readnone speculatable willreturn
declare { i64, i1 } @llvm.ssub.with.overflow.i64(i64, i64) #0

; Function Attrs: nocallback nofree nosync nounwind readnone speculatable willreturn
declare i64 @llvm.ctpop.i64(i64) #0

attributes #0 = { nocallback nofree nosync nounwind readnone speculatable willreturn }

!0 = !{i64 4202496}
