#include "llvm/Pass.h"
#include "llvm/IR/Module.h"
#include "llvm/IR/Function.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/IR/Type.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/Instruction.h"
#include "llvm/IR/LLVMContext.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/IR/IRBuilder.h"
#include <vector>

using namespace llvm;

namespace{
struct SkeletonPass : public ModulePass{
    static char ID;
    //Function *raplread;   // this will be the identifier for the rapl read function
    Function *monitor; 
    Function *monitor_2; 
    SkeletonPass() : ModulePass(ID) {}

    virtual bool runOnModule(Module &M)
    {

        BasicBlock::iterator B_last;
        BasicBlock::iterator BF_ins;
        BasicBlock::iterator BF_ins_2;
        BasicBlock::iterator BF_ins_3;
        BasicBlock::iterator BF_ins_4;
        Function::iterator F_last;


        for(Module::iterator L= M.begin(), K = M.end(); L!= K; ++L)
        {

            if(L->getName() == "print_1"){
                monitor = cast<Function>(L);
                break;
                
            }
        }

        for(Module::iterator L= M.begin(), K = M.end(); L!= K; ++L)
        {

            if(L->getName() == "print_2"){
                monitor_2 = cast<Function>(L);
                break;
                
            }
        }

        for(Module::iterator F = M.begin(), E = M.end(); F!= E; ++F)
        {
            if(F->getName() == "print_1"){
                
                continue;
            }
           
            
            bool last_inst =false;
            bool prev_last = false ;
            for(Function::iterator BB = F->begin(), E = F->end(); BB != E; ++BB)
            {

                        int count =0 ;
                        int count_temp =0 ;
                        bool just_entered =false;
                        count = std::distance(BB->begin(), BB->end());
                        errs() << count << " \n";
                        for (BasicBlock::iterator I = BB->begin(), IE = BB->end(); I != IE; ++I) {
                            count_temp++;
                            if ((llvm::isa <llvm::CallInst> (I))){
                                if (count_temp<count){ //intermidiate inst of bb
                                    errs() << "Case 1  \n";
                                    Instruction *inst1 = &*I;
                                    IRBuilder<> builder1(inst1);
                                    //Value *v = builder1.CreateGlobalStringPtr(BB->getName(), "str");
                                    //ArrayRef<Value *> args(v);
                                    Instruction *newInst1 = CallInst::Create(monitor_2,  "");    // create the first insttruction to be added : a call to the print function
                                    BB->getInstList().insert(I, newInst1);    
                                    if (!just_entered ){
                                        just_entered =true;}
                                    else{
                                        just_entered =true;
                                        Instruction *inst2 = &*I;
                                        IRBuilder<> builder2(inst2);
                                        Instruction *newInst2 = CallInst::Create(monitor_2,  "");    // create the first insttruction to be added : a call to the print function
                                        BB->getInstList().insert(I, newInst2); 
                                    } 

                                }
                                else {
                                    errs() << "Case 2  \n";
                                    Instruction *inst3 = &*I;
                                    IRBuilder<> builder3(inst3);
                                    Instruction *newInst3 = CallInst::Create(monitor_2,  "");    // create the first insttruction to be added : a call to the print function
                                   
                                    BB->getInstList().insert(I, newInst3);  
                                    last_inst =true;
                                    //newInst3->insertAfter(inst3);
                                    
                                    //BasicBlock *pb = &*BB;
                                    //pb->getInstList().push_back(newInst3);
                                }
                            }
                            else {
                                    if (count_temp==count) {last_inst=false;}// In this case the last inst is not a call inst
                                    if (just_entered ){ // in this case the previous inst was a call so a new call to monitor has to be added
                                        just_entered =false;
                                        Instruction *inst2 = &*I;
                                        IRBuilder<> builder2(inst2);
                                        Instruction *newInst2 = CallInst::Create(monitor_2,  "");    // create the first insttruction to be added : a call to the print function
                                        BB->getInstList().insert(I, newInst2); 
                                    } 
                            }
                        }
                            /*if( BF_ins_2!= IE){errs() << "LLLLLLLLLLLLLLLLLLLLLLLLLLLL\n";}
                            if (llvm::isa <llvm::CallInst> (I)){
                                
                                Instruction *inst_2 = &*BF_ins;
                                errs() << "new print_2 instr AAAAAAAAAAAA\n";
                                IRBuilder<> builder_2(inst_2);
                                Value *v2 = builder_2.CreateGlobalStringPtr(BB->getName(), "str");
                                ArrayRef<Value *> args_2(v2);
                                //Instruction *newInst_2 = CallInst::Create(monitor_2, args_2, "");    // create the first insttruction to be added : a call to the print function
                                //BB->getInstList().insert(BF_ins, newInst_2);                         // we give as argument the name of the bb and we insert it at the beggining f the bb

                                
                                //Instruction *inst_3 = &*(BF_ins--);
                                //errs() << "new print_2 instr AAAAAAAAAAAA\n";
                                //IRBuilder<> builder_3(inst_3);
                                //Value *v3 = builder_3.CreateGlobalStringPtr(BB->getName(), "str");
                                //ArrayRef<Value *> args_3(v3);
                                //Instruction *newInst_3 = CallInst::Create(monitor_2, args_3, "");    // create the first insttruction to be added : a call to the print function
                                

                               
                                errs() << "nXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX\n";
                                Instruction *inst_3 = &*(I);
                                errs() << "new print_2 instr AAAAAAAAAAAA\n";
                                IRBuilder<> builder_3(inst_3);
                                Value *v3 = builder_3.CreateGlobalStringPtr(BB->getName(), "str");
                                ArrayRef<Value *> args_3(v3);
                                Instruction *newInst_3 = CallInst::Create(monitor_2, args_3, ""); 
                                
                                //else {
                                        
                                 //   BF_ins++;
                                 //   BB->getInstList().insert(BF_ins, newInst_2);  

                                //}
*/                  
                    BasicBlock::iterator BI = BB->begin();     // BI will hold the begging point  of the basic block so that we can insert instructions there
                    BasicBlock::iterator BF = BB->end();
                    
                    
                     if(prev_last)  {    //Checkif last inst is call so we have to add call now 
                        Instruction *inst5 = &*BI;
                        IRBuilder<> builder5(inst5);
                        Instruction *newInst5 = CallInst::Create(monitor_2,  "");    // create the first insttruction to be added : a call to the print function
                        BB->getInstList().insert(BI, newInst5); 

                    }     
                    prev_last = last_inst; 
                    
                    
                    BF--;                                      // BF will hold the ending point  of the basic block so that we can insert instructions there
                    B_last = BF;
                    F_last = BB;
                    errs() << "new basic block\n";
                    BB->setName(F->getName());                // set the name of the bb to its function name plus a unique number which will be added automatically . for more check read.ME
                   
                    errs() << "Basic Block name: " << BB->getName() << "\n";
                    errs()<< "Of function : " << F->getName() << "\n";  // print the name of the current BB
                    errs() << *BB;                                            // print the contents of the bb in the form of llvm IR assembly instructions
                    
                    Instruction *inst = &*BI;
                    IRBuilder<> builder(inst);
                    Value *v = builder.CreateGlobalStringPtr(BB->getName(), "str");
                    ArrayRef<Value *> args(v);
                    Instruction *newInst = CallInst::Create(monitor, args, "");    // create the first insttruction to be added : a call to the print function
                    BB->getInstList().insert(BI, newInst);                         // we give as argument the name of the bb and we insert it at the beggining f the bb
                    /*
                    Instruction *newInst0 = CallInst::Create(raplread, "");      //create the second instruction to be added : a call to the readrapl function which reads rapl energy
                    BB->getInstList().insert(BI, newInst0);                       // we insert it at the beggining of the basic block and it will print two energy values
                    
                    Instruction *newInst1 = CallInst::Create(raplread, "");     //create the third instruction to be added : a call to the readrapl function which reads rapl energy
                    BB->getInstList().push_back(newInst1);                     // we insert it at the end of the basic block and it will print two energy values
                      */  

                          

                
            }
        }

        Instruction *inst0 = &*B_last;
                    IRBuilder<> builder(inst0);
                    Value *v1 = builder.CreateGlobalStringPtr("final  ", "str");
                    ArrayRef<Value *> args(v1);
                    Instruction *newInst0 = CallInst::Create(monitor, args, "");    // create the first insttruction to be added : a call to the print function
                    F_last->getInstList().insert(B_last, newInst0);  
                    

       /*Module::iterator M_last = M.end();           //we find the last function of the module
        M_last-- ;
        errs() << "0\n";
        Function::iterator F_last = M_last->end();   // we find the last BB of the last function of the module
        F_last--;
        errs() << F_last->getName();
        BasicBlock::iterator BB_last= F_last->end();  // we find the last instruction of the last BB of the last function  of the module
        BB_last--;
        errs() << "02\n";
        Instruction *inst0 = &*BB_last;
        errs() << "1\n";
        IRBuilder<> builder1(inst0);
        errs() << "2\n";
        Value *v1 = builder1.CreateGlobalStringPtr(F_last->getName(), "str");
        errs() << "3\n";
        ArrayRef<Value *> args(v1);
        errs() << "4\n";
        Instruction *newInst0 = CallInst::Create(monitor, args, "");    // create the first insttruction to be added : a call to the print function
        errs() << "5\n";
        F_last->getInstList().push_back(newInst0);                         // we give as argument the name of the bb and we insert it at the beggining f the bb
              errs() << "6\n";

        
*/


        return true;
    }
};
}

char SkeletonPass::ID = 0;
static RegisterPass<SkeletonPass> X("skeleton", "LLVM IR Instrumentation Pass");

